import nflreadpy as nfl
import polars as pl
import pandas as pd


player = "Patrick Mahomes"
year = 2025
week = 15
fantasy_pos = ["QB","RB", "WR", "TE"]

player_stats = nfl.load_player_stats(seasons=[year])

# print(player_stats.describe())
# print(player_stats.glimpse())

target_stats = (
    player_stats.filter(pl.col("position").is_in(fantasy_pos))
    .with_columns(
        game_count = pl.len().over("player_id")
    )
    .filter(pl.col("game_count") >= 10)
    .drop("game_count")
    )

target_stats.write_csv("player_season.csv")