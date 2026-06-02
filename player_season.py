import nflreadpy as nfl
import polars as pl
import pandas as pd
import Download

player = "Patrick Mahomes"
year = 2025
week = 15

player_stats = nfl.load_player_stats(seasons=[year])

# print(player_stats.describe())
# print(player_stats.glimpse())

target_stats = player_stats.filter(pl.col("player_display_name") == player)
print(target_stats)

print(target_stats.glimpse())