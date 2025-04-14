"""Unreal Engine Asset Scanner and Database.

Attributes:
    TABLE_NAME: Name of the SQLite database table where asset metadata will be stored.
    ASSET_FIELDS: List of asset metadata fields stored in the database.

Note:
    This script should be run within the Unreal Engine Python environment.
"""

import datetime
import json
import sqlite3
from pathlib import Path
from queue import Queue
from threading import Thread

import unreal

TABLE_NAME = "game_content"
ASSET_FIELDS = [
    "asset_name",
    "asset_class",
    "ue_file_path",
    "dependencies",
    "referencers",
    "tag_values",
    "file_size_mb",
    "last_mod_time",
    "disk_file_path",
    "is_asset_loaded",
    "is_redirector",
    "is_u_asset",
    "is_valid",
    "asset_class_path",
]


class GameContentDB:
    """Database manager for Unreal game content assets."""

    def __init__(self, db_file_path: str | Path) -> None:
        unreal.log(f"Initializing DB at: {db_file_path}")
        self.conn = sqlite3.connect(db_file_path, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")  # reset table
        self._initialize_schema()
        self.queue = Queue()
        self.worker = Thread(target=self._db_writer, daemon=True)
        self.worker.start()

    def _initialize_schema(self) -> None:
        """Initialize the database schema for game content assets."""
        fields_def = ", ".join([f"{field} TEXT NOT NULL" for field in ASSET_FIELDS])
        schema = f"""
        CREATE TABLE {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {fields_def},
            UNIQUE(ue_file_path)
        );
        """
        with self.conn:
            self.conn.executescript(schema)

    def _db_writer(self) -> None:
        """Background thread to handle DB inserts."""
        batch = []
        while True:
            item = self.queue.get()
            if item is None:
                if batch:  # process any remaining items
                    self._insert_batch(batch)
                break
            batch.append(item)
            if len(batch) >= 10:  # adjust batch size (e.g., 10-50)
                self._insert_batch(batch)
                batch = []
            self.queue.task_done()
        if batch:  # ensure no items are left
            self._insert_batch(batch)

    def _insert_batch(self, batch: list[tuple[str, ...]]) -> None:
        """Insert a batch of items into the database.

        Performs bulk insertion of multiple asset records into the database
        using SQLite's executemany for better performance.

        Args:
            batch: List of tuples, each containing asset field values in
                    the same order as ASSET_FIELDS.

        """
        placeholders = ", ".join(["?" for _ in ASSET_FIELDS])
        try:
            with self.conn:
                self.conn.executemany(
                    f"""
                    INSERT OR IGNORE INTO {TABLE_NAME} ({", ".join(ASSET_FIELDS)})
                    VALUES ({placeholders})
                    """,
                    batch,
                )
        except Exception as e:
            unreal.log_error(f"Batch insert failed: {e}")

    def insert_asset(self, **kwargs: str) -> None:
        """Queue asset data for background insertion.

        Takes asset metadata as keyword arguments and adds them to the queue
        for processing by the background worker thread.

        Args:
        **kwargs: Asset metadata fields matching ASSET_FIELDS.

        """
        # ensure all fields are provided in the correct order
        item = tuple(kwargs.get(field) for field in ASSET_FIELDS)
        self.queue.put(item)

    def close(self) -> None:
        """Stop the worker and close the DB."""
        self.queue.put(None)  # signal worker to stop
        self.worker.join()  # wait for worker to exit
        self.conn.close()  # close db connection
        unreal.log("DB closed")


class GameContentScanner:
    """Scanner for Unreal Engine game content assets."""

    def __init__(self, ue_folder_path: str, db_file_path: str | Path) -> None:
        """Initialize the game content scanner.

        Args:
            ue_folder_path: Unreal Engine content path to scan. (ex. "/Game/StarterContent/")
                The "content" folder for a standard project is "/Game/".
            db_file_path: File path for SQLite database. DB file will be created if absent.

        """
        self.ue_folder_path = ue_folder_path
        self.db = GameContentDB(db_file_path)
        self.asset_paths = None
        self.index = 0
        self.batch_size = 10
        self.tick_handle = unreal.register_slate_post_tick_callback(self.tick)

    def start(self) -> None:
        """Begin the asset scanning process."""
        unreal.log(f"Starting scanning: {self.ue_folder_path}")
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        if asset_registry.is_loading_assets():
            unreal.log("Waiting for asset registry...")
            while asset_registry.is_loading_assets():
                pass
        self.asset_paths = unreal.EditorAssetLibrary.list_assets(
            self.ue_folder_path,
            recursive=True,
        )
        unreal.log(f"Found {len(self.asset_paths)} assets")

    def tick(self, delta_time: float) -> None:
        """Process a batch of assets on each Unreal tick.

        Args:
            delta_time: Time in seconds since the last tick. (unused)

        """
        if not self.asset_paths or self.index >= len(self.asset_paths):
            self.finish()
            return

        end_index = min(self.index + self.batch_size, len(self.asset_paths))
        for i in range(self.index, end_index):
            asset_path = self.asset_paths[i]
            metadata = self.get_asset_metadata(asset_path)
            if metadata:
                self.db.insert_asset(**metadata)
        self.index = end_index
        unreal.log(f"Processed {self.index}/{len(self.asset_paths)} assets")

    def finish(self) -> None:
        """Cleanly terminate the scanning process."""
        unreal.unregister_slate_post_tick_callback(self.tick_handle)
        self.db.queue.join()  # wait for all queued assets to be written
        self.db.close()  # close the db
        unreal.log(f"Finished scanning {self.ue_folder_path}")

    @staticmethod
    def resolve_asset_file_path(package_name: str) -> Path | None:
        """Resolves the full disk file path of an Unreal asset given its package name.

        Args:
            package_name: Asset's package name.
                (ex. "/Game/StarterContent/Props/Materials/M_Chair")

        Returns:
            File path to the asset. (.uasset or .umap)

        """
        project_content_dir = unreal.Paths.convert_relative_path_to_full(
            unreal.Paths.project_content_dir(),
        )
        file_path = project_content_dir + str(package_name).replace("/Game", "")
        for ext in [".uasset", ".umap"]:
            asset_file_path = Path(file_path + ext)
            if asset_file_path.exists():
                return asset_file_path
        return None

    @staticmethod
    def get_pc_metadata(asset_data: unreal.AssetData) -> tuple[float, str, Path]:
        """Extracts file size (in MB), last modification timestamp, and disk file path string.

        Args:
            asset_data: Holds important information about an asset.
                Returned from "EditorAssetLibrary.find_asset_data(asset_path)".

        Returns:
                - File size in MB.
                - Last modified time. (YYYY-MM-DD HH:MM:SS)
                - Full disk file path.

        """
        package_name = asset_data.package_name
        asset_file_path = GameContentScanner.resolve_asset_file_path(package_name)
        if not asset_file_path:
            unreal.log_warning(f"File not found for package: {package_name}")
            return 0.0, "", Path()

        try:
            file_size_mb = round(asset_file_path.stat().st_size / (1024 * 1024), 3)
            mtime = asset_file_path.stat().st_mtime
            last_mod_time = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            return file_size_mb, last_mod_time, asset_file_path
        except Exception as e:
            unreal.log_error(f"Error accessing {asset_file_path}: {e}")
            return 0.0, "", Path()

    @staticmethod
    def get_asset_metadata(asset_path: str) -> dict[str, str]:
        """Collects metadata for a given Unreal asset path.

        Args:
            asset_path: Unreal asset path.
                (ex. "/Game/StarterContent/Props/SM_Chair.SM_Chair")

        Returns:
            A dictionary with metadata fields for the asset.

        """
        # initialize default values
        metadata = dict.fromkeys(ASSET_FIELDS, "")

        asset_data = unreal.EditorAssetLibrary.find_asset_data(asset_path)
        if not asset_data:
            unreal.log(f"No asset_data for: {asset_path}")
            return metadata

        metadata["asset_name"] = str(asset_data.asset_name)
        metadata["asset_class"] = str(asset_data.asset_class_path.asset_name)
        metadata["asset_class_path"] = str(asset_data.asset_class_path.package_name)
        metadata["ue_file_path"] = str(asset_data.package_name)

        metadata["is_asset_loaded"] = str(asset_data.is_asset_loaded())
        metadata["is_redirector"] = str(asset_data.is_redirector())
        metadata["is_u_asset"] = str(asset_data.is_u_asset())
        metadata["is_valid"] = str(asset_data.is_valid())

        metadata["tag_values"] = str(unreal.EditorAssetLibrary.get_tag_values(asset_path))

        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        dep_options = unreal.AssetRegistryDependencyOptions()
        raw_dependencies = asset_registry.get_dependencies(metadata["ue_file_path"], dep_options)
        metadata["dependencies"] = json.dumps(
            [str(dep) for dep in raw_dependencies] if raw_dependencies else [],
        )
        raw_referencers = asset_registry.get_referencers(metadata["ue_file_path"], dep_options)
        metadata["referencers"] = json.dumps(
            [str(dep) for dep in raw_referencers] if raw_referencers else [],
        )

        metadata["file_size_mb"] = str(GameContentScanner.get_pc_metadata(asset_data)[0])
        metadata["last_mod_time"] = GameContentScanner.get_pc_metadata(asset_data)[1]
        metadata["disk_file_path"] = Path(
            GameContentScanner.get_pc_metadata(asset_data)[2],
        ).as_posix()  # convert to forward slashes

        return metadata


# entry Point
def main(ue_folder_path: str, db_file_path: str | Path) -> None:
    """Entry point for scanning Unreal Engine game content.

    Args:
        ue_folder_path: Unreal Engine content path to scan. (ex. "/Game/StarterContent/")
            The "content" folder for a standard project is "/Game/".
        db_file_path: File path for SQLite database. DB file will be created if absent.

    """
    scanner = GameContentScanner(ue_folder_path, db_file_path)
    scanner.start()


if __name__ == "__main__":
    ue_folder_path = "/Game/"  # ue content folder
    db_file_path = Path(__file__).parent / "data" / f"{TABLE_NAME}.db"
    main(ue_folder_path, db_file_path)
