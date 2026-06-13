import nflreadpy as nfl
import polars as pl

#function that returns history for player/s from a range
def get_team_history(year=2025):
    #loads history from the range
    history = nfl.load_team_stats(seasons=year)
    if "game_id" not in history.columns:
        history = history.with_columns(
            pl.concat_str([pl.col("season"), pl.lit("_"), pl.col("week"), pl.lit("_"), pl.col("team"), pl.lit("_"), pl.col("opponent_team")])
            .alias("game_id")
        )

    print(f"Successfully pulled team statistics for {year}!")
    return history

team_history_list = []
drop_cols = [
    "fg_made", "fg_att", "fg_missed", "fg_blocked", "fg_long", "fg_pct", "fg_made_0_19", "fg_made_20_29", "fg_made_30_39", "fg_made_40_49", 
    "fg_made_50_59", "fg_made_60_", "fg_missed_0_19", "fg_missed_20_29", "fg_missed_30_39", "fg_missed_40_49", "fg_missed_50_59", "fg_missed_60_", 
    "fg_made_list", "fg_missed_list", "fg_blocked_list", "fg_made_distance", "fg_missed_distance", "fg_blocked_distance", "pat_made", "pat_att", 
    "pat_missed", "pat_blocked", "pat_pct", "gwfg_made", "gwfg_att", "gwfg_missed", "gwfg_blocked", "gwfg_distance"
]

years = range(2025,1999, -1)
for y in years:
    year_data = get_team_history(y).drop(drop_cols)

    if year_data is not None and year_data.height > 0:
        team_history_list.append(year_data)

team_history_df = pl.concat(team_history_list, how="diagonal_relaxed")
team_history_df.write_csv("team_history.csv")