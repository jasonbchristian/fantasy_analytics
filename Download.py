import nflreadpy as nfl
import polars as pl
import pandas as pd

# Load current season play-by-play data
pbp = nfl.load_pbp(2025)

# # Load player game-level stats for multiple seasons
player_stats = nfl.load_player_stats([2024, 2025])

# # Load all available team level stats
# team_stats = nfl.load_team_stats(seasons=True)
