import nflreadpy as nfl
import polars as pl
import pandas as pd

depth = nfl.load_depth_charts()
cols = ["team", "player_name", "pos_abb", "pos_rank"]
fantasy_pos = ["QB","RB", "WR", "TE"]
team = ["TB"]
# print(depth.glimpse())



# positions = depth.filter(pl.col("pos_abb").is_in(fantasy_pos) & pl.col("team").is_in(team))
positions = depth.filter(pl.col("pos_abb").is_in(fantasy_pos))
latest_date = positions.select(pl.col("dt").max()).item()

positions = positions.filter(
    (pl.col("dt") == latest_date) & 
    (pl.col("pos_rank") <= 3))

positions = positions.select(pl.col(cols)).sort(["team", "pos_abb", "pos_rank"])

positions.write_csv("depth.csv")