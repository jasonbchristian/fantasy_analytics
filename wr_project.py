import nflreadpy as nfl
import polars as pl
import get_depth as gd
import get_player_history as ph

current_wrs = gd.get_depth(position=["WR"], depth=4)
wr_list = current_wrs["gsis_id"].to_list()
wr_history_list = []
for y in range(2025, 1999, -1):
    year_data = ph.get_player_history(player_ids=wr_list, position=["WR"], year=y)

    if year_data is not None and year_data.height > 0:
        wr_history_list.append(year_data)
    
wr_history_df = pl.concat(wr_history_list)
wr_history_df.write_csv("wr_history.csv")