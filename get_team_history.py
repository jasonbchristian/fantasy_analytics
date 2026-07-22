import nflreadpy as nfl
import polars as pl
from sqlalchemy import create_engine
import polars.selectors as cs

#function that returns game history for a given year
def get_team_history(year=2025):
    #loads history from the range
    history = nfl.load_team_stats(seasons=year)
    #assigns a game_id if absent
    if "game_id" not in history.columns:
        history = history.with_columns(
            pl.concat_str([pl.col("season"), pl.lit("_"), pl.col("week"), pl.lit("_"), pl.col("team"), pl.lit("_"), pl.col("opponent_team")])
            .alias("game_id")
        )
    print(f"Successfully pulled team history for {year}!")
    return history