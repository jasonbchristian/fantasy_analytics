import sqlite3

def delete_last_10_rows(db_path="football.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Identify the 10 most recent game_ids to delete
    # Note: We use ORDER BY game_id DESC to get the latest ones
    delete_sql = """
    DELETE FROM team_game_data 
    WHERE game_id IN (
        SELECT game_id FROM team_game_data 
        ORDER BY game_id DESC 
        LIMIT 10
    );
    """
    
    cursor.execute(delete_sql)
    print(f"Deleted {cursor.rowcount} rows from the database.")
    
    conn.commit()
    conn.close()


delete_last_10_rows()