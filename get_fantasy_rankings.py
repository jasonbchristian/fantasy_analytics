import nflreadpy as nfl
import polars as pl
import pandas as pd

ff_rank = nfl.load_ff_rankings() 
fantasy_pos = ["QB","RB", "WR", "TE"]

print(ff_rank.glimpse())

ff_rank = ff_rank.filter((pl.col("team")=="TB") & pl.col("pos").is_in(fantasy_pos))

ff_rank.write_csv("ff_rankings.csv")