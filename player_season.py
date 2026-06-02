import polars as pl
import Download

player = "Patrick Mahomes"
year = 2025
week = 15

Download.pbp.filter(pl.col("passer_player_name") == player)
player_summary = player_plays.select([
    "game_id", "week", "down", "ydstogo", "yards_gained", "epa", "desc"
])

print(player_summary.head())