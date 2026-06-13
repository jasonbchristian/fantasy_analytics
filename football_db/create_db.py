import sqlite3

sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS team_game_data ( 
            game_id TEXT, team TEXT, season INTEGER,week INTEGER,season_type TEXT,opponent_team TEXT,
            
            completions REAL,attempts REAL,passing_yards REAL,passing_tds REAL,passing_interceptions REAL,sacks_suffered REAL,sack_yards_lost REAL,sack_fumbles REAL,
            sack_fumbles_lost REAL,passing_air_yards REAL,passing_yards_after_catch REAL,passing_first_downs REAL,passing_epa REAL,passing_cpoe REAL,passing_2pt_conversions REAL,

            carries REAL,rushing_yards REAL,rushing_tds REAL,rushing_fumbles REAL,rushing_fumbles_lost REAL,rushing_first_downs REAL,rushing_epa REAL,rushing_2pt_conversions REAL,
            
            receptions REAL,targets REAL,receiving_yards REAL,receiving_tds REAL,receiving_fumbles REAL,receiving_fumbles_lost REAL,receiving_air_yards REAL,
            receiving_yards_after_catch REAL,receiving_first_downs REAL,receiving_epa REAL,receiving_2pt_conversions REAL,

            special_teams_tds REAL,def_tackles_solo REAL,def_tackles_with_assist REAL,def_tackle_assists REAL,def_tackles_for_loss REAL,def_tackles_for_loss_yards REAL,
            def_fumbles_forced REAL,def_sacks REAL,def_sack_yards REAL,def_qb_hits REAL,def_interceptions REAL,
            def_interception_yards REAL,def_pass_defended REAL,def_tds REAL,def_fumbles REAL,def_safeties REAL,

            
            misc_yards REAL,fumble_recovery_own REAL,fumble_recovery_yards_own REAL,fumble_recovery_opp REAL,fumble_recovery_yards_opp REAL,fumble_recovery_tds REAL,
            penalties REAL,penalty_yards REAL,timeouts REAL,punt_returns REAL,punt_return_yards REAL,kickoff_returns REAL,kickoff_return_yards REAL,

            PRIMARY KEY (game_id, team)
        );"""
]

# create a database connection
try:
    with sqlite3.connect('football_db/football.db') as conn:
        # create a cursor
        cursor = conn.cursor()

        # execute statements
        for statement in sql_statements:
            cursor.execute(statement)

        # commit the changes
        conn.commit()

        print("Tables created successfully.")
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
