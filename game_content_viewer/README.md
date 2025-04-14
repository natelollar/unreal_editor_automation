# Inventory Unreal 5 /Content Folder
- Run game_content_scanner.py via Unreal's Python console.
- Simply copy the game_content_scanner.py file path into the Unreal Python console.
    - This produces a .db file listing all the objects in the Unreal /Content folder.
    - This game_content.db file will output to the /data folder.
        - DB Browser helpful for viewing .db files.
        - https://sqlitebrowser.org/dl/

- Run game_content_summary.py next, to create a table summarizing Unreal content gathered.
    - Does not require Unreal Python console.

- Run convert_db_to_csv.py to get a .csv verision of the .db tables.
    - Does not require Unreal Python console.

---
- Update paths in launch_game.exe
    - Useful for launching Unreal project quickly.

