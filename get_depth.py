import nflreadpy as nfl
import polars as pl
from datetime import date

# most recent depth chart for all NFL teams

def get_depth(y = 2026,position = None, team = None, depth = None):
    #defines relevant columns and positions
    if position == None:
        position = {"QB":2, "WR":4, "RB":3, "TE":2}
 
    #loads full depth chart and finds most recent version
    full_depth = nfl.load_depth_charts(y)

    #creates year column, drops irrelevent cols, filters out to unique rows
    full_depth = full_depth.with_columns(pl.col("dt").dt.year().alias("year"))
    full_depth = full_depth.drop(["dt", "pos_grp", "pos_id", "pos_grp_id","pos_name", "pos_slot"])
    full_depth = full_depth.unique()

    #filters down to relevant positions and most recent depth chart
    depth_chart = (
        full_depth
        .filter(
            (pl.col("pos_abb").is_in(list(position.keys())) 
            & pl.col("pos_rank")<= pl.col("pos_abb").replace_strict(position, default=None,return_dtype="i32")) 
        )
        .sort(["team", "pos_abb", "pos_rank", "player_name"])
    )
    
    #pulls depth for specified team/s
    if team is not None:
        depth_chart = depth_chart.filter(pl.col("team").is_in(team))
    
    #filters to only pull through depth = d
    if depth is not None:
        depth_chart = depth_chart.filter(pl.col("pos_rank") <= depth)
    
    print(f"Depth chart from {y} successfully pulled!")
    return depth_chart

res = get_depth(depth=4)
res.write_csv("library/depth.csv")

