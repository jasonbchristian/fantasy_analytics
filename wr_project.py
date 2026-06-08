import nflreadpy as nfl
import polars as pl
import get_depth as gd
import get_player_history as ph
import get_team_history as th
from sklearn.model_selection import train_test_split

current_wrs = gd.get_depth(position=["WR"], depth=4)
wr_list = current_wrs["gsis_id"].to_list()
wr_history_list = []
for y in range(2025, 1999, -1):
    year_data = ph.get_player_history(player_ids=wr_list, position=["WR"], year=y)

    if year_data is not None and year_data.height > 0:
        wr_history_list.append(year_data)
wr_history_df = pl.concat(wr_history_list)

team_history_list = []
for y in range(2025, 1999, -1):
    year_data = th.get_team_history(year=y)

    if year_data is not None and year_data.height > 0:
        team_history_list.append(year_data)

team_history_df = pl.concat(team_history_list, how="diagonal_relaxed")
print(team_history_df.null_count().glimpse())

# player_team_stats = wr_history_df.join(team_history, on="team_id")

wr_history_df.write_csv("library/wr_history.csv")
team_history_df.write_csv("library/team_history.csv")
# features = 
# X = wr_history_df []
# y = wr_history_df ["fantasy_points_ppr"] 

# X_train, X_test,
# y_train, y_test = train_test_split(X, y, random_state=42, test_size= 0.20)

