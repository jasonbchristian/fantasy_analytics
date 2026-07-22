import get_team_history as th
import get_player_history as ph
import get_depth as gd
import nflreadpy as nfl
import polars as pl
from sqlalchemy import create_engine
import polars.selectors as cs
engine = create_engine('sqlite:///football_db/football.db', echo=False)
#fills in nulls and NANs as 0s
def check_nulls_nans(df):
    df = df.fill_null(0).fill_nan(0)
    # nans = df.select(cs.numeric()).select(pl.all().is_nan().sum())
    # print("NaN counts per column:")
    # print(nans.glimpse())
    # nulls = df.null_count()
    # print("\nNull counts per column:")
    # print(nulls.glimpse())
    return df

#retrieves team-wide game data for all years
def fetch_all_games():
    #load existing game data
    existing = pl.read_database(query= "SELECT game_id, team FROM team_game_data" , connection=engine.connect())
    
    #pull new game data from api
    new_list = []
    drop_cols = [
        "fg_made", "fg_att", "fg_missed", "fg_blocked", "fg_long", "fg_pct", "fg_made_0_19", "fg_made_20_29", "fg_made_30_39", "fg_made_40_49", 
        "fg_made_50_59", "fg_made_60_", "fg_missed_0_19", "fg_missed_20_29", "fg_missed_30_39", "fg_missed_40_49", "fg_missed_50_59", "fg_missed_60_", 
        "fg_made_list", "fg_missed_list", "fg_blocked_list", "fg_made_distance", "fg_missed_distance", "fg_blocked_distance", "pat_made", "pat_att", 
        "pat_missed", "pat_blocked", "pat_pct", "gwfg_made", "gwfg_att", "gwfg_missed", "gwfg_blocked", "gwfg_distance"
    ]
    
    #pulls games from each year and filters out against the existing db
    for y in range(2025,1999, -1):
        year_data = th.get_team_history(y).drop(drop_cols)
        if year_data is not None and year_data.height > 0:
            filtered_year = year_data.join(existing, on=["game_id","team"], how="anti")
            if filtered_year.height > 0:
                new_list.append(filtered_year)
                print(f"Successfully pulled team statistics for {y}!")

    #writes new games to db
    if len(new_list) > 0:
        new_df = pl.concat(new_list, how="diagonal_relaxed")
        new_df = check_nulls_nans(new_df)
        new_df.write_csv("team_history_new.csv")
        new_df.write_database("team_game_data", connection=engine, if_table_exists="append")

    else:
        print("No new games found. Game database is up to date.")

def fetch_all_players():
    #load existing player data
    existing = pl.read_database(query= "SELECT game_id, team FROM player_game_data" , connection=engine.connect())
    
    #pull new game data from api
    new_list = []
    drop_cols = [
    ]
    positions = ["QB", "WR", "RB", "TE"]
    #pulls games from each year and filters out against the existing db
    for y in range(2025,1999, -1):
        year_data = ph.get_player_history(player_ids=wr_list, position=positions, year=y).drop(drop_cols)
        if year_data is not None and year_data.height > 0:
            filtered_year = year_data.join(existing, on=["game_id","team"], how="anti")
            if filtered_year.height > 0:
                new_list.append(filtered_year)
                print(f"Successfully pulled team statistics for {y}!")

    #writes new games to db
    if len(new_list) > 0:
        new_df = pl.concat(new_list, how="diagonal_relaxed")
        new_df = check_nulls_nans(new_df)
        new_df.write_csv("player_history_new.csv")
        new_df.write_database("team_game_data", connection=engine, if_table_exists="append")

    else:
        print("No new games found. Game database is up to date.")


def fetch_all_depth():
    #load existing depth data
    existing = pl.read_database(
        query= "SELECT team, espn_id, pos_rank, year FROM depth_chart" , 
        connection=engine.connect(),
        schema_overrides = {
        "team": pl.String,
        "espn_id": pl.String,
        "pos_rank": pl.Int32,
        "year": pl.Int32
    }
        )
    
    new_list = []
    #pulls games from each year and filters out against the existing db
    for y in range(2026,1999, -1):
        year_data = gd.get_depth(y)
        if year_data is not None and year_data.height > 0:
            filtered_year = year_data.join(existing, on=["espn_id","team", "year", "pos_rank"], how="anti")
            if filtered_year.height > 0:
                new_list.append(filtered_year)
                print(f"Successfully pulled team statistics for {y}!")

    #writes new games to db
    if len(new_list) > 0:
        new_df = pl.concat(new_list, how="diagonal_relaxed")
        new_df = check_nulls_nans(new_df)
        new_df.write_csv("depth.csv")
        new_df.write_database("depth_chart", connection=engine, if_table_exists="append")

    else:
        print("No new games found. Game database is up to date.")


# def fetch_new_games():

# res = fetch_all_games()
res = fetch_all_depth()
# team_history_df.write_database(table_name="team_game_data", connection=engine.connect(), if_table_exists = "append" )