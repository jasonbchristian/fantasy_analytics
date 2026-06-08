import nflreadpy as nfl
import polars as pl

# most recent depth chart for all NFL teams

def get_depth(position = None, team = None, depth = None):
    #defines relevant columns and positions
    if position == None:
        position = ["QB", "WR", "RB", "TE"]
    cols = ["team", "player_name", "gsis_id", "pos_abb", "pos_rank"]

    #loads full depth chart and finds most recent version
    full_depth = nfl.load_depth_charts()
    # The .item() belongs here, after the selection
    latest_depth = full_depth.select(pl.col("dt").max()).item()

    #filters down to relevant positions and most recent depth chart
    depth_chart = (
        full_depth.filter(
            (pl.col("pos_abb").is_in(position)) &
            (pl.col("dt") == latest_depth)
        )
        .select(pl.col(cols))
        .sort(["team", "pos_abb", "pos_rank"])
    )
    
    #pulls depth for specified team/s
    if team is not None:
        depth_chart = depth_chart.filter(pl.col("team").is_in(team))
    
    #filters to only pull through depth = d
    if depth is not None:
        depth_chart = depth_chart.filter(pl.col("pos_rank") <= depth)
    
    print("Depth chart successfully pulled!")
    return depth_chart

res = get_depth(position=["WR"], depth=4)
res.write_csv("library/depth.csv")

