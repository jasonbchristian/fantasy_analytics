import nflreadpy as nfl
import polars as pl
import get_depth as gd
import get_player_history as ph
import get_team_history as th
from sklearn.model_selection import train_test_split

# pull latest depth chart for WRs
current_wrs = gd.get_depth(position=["WR"], depth=4)

#pulls game stats for all years for each individual wr using player id
wr_list = current_wrs["gsis_id"].to_list()
wr_history_list = []
for y in range(2025, 1999, -1):
    year_data = ph.get_player_history(player_ids=wr_list, position=["WR"], year=y)

    if year_data is not None and year_data.height > 0:
        wr_history_list.append(year_data)
wr_history_df = pl.concat(wr_history_list)

#pulls game stats for all years
team_history_list = []
for y in range(2025, 1999, -1):
    year_data = th.get_team_history(year=y)

    if year_data is not None and year_data.height > 0:
        team_history_list.append(year_data)

team_history_df = pl.concat(team_history_list, how="diagonal_relaxed")

#narrows to relevent columns for WRs
rel_cols = [
    "season","week","team","season_type","game_id","opponent_team","completions","attempts","passing_yards","passing_tds","passing_interceptions","sacks_suffered","sack_yards_lost",
    "sack_fumbles","sack_fumbles_lost","passing_air_yards","passing_yards_after_catch","passing_first_downs","passing_epa","passing_cpoe",
    "carries","rushing_yards","rushing_tds","rushing_fumbles","rushing_fumbles_lost","rushing_first_downs","rushing_epa",
    "receptions","targets","receiving_yards","receiving_tds","receiving_fumbles","receiving_fumbles_lost","receiving_air_yards","receiving_yards_after_catch","receiving_first_downs","receiving_epa",
    "def_tackles_solo","def_tackles_with_assist","def_tackle_assists","def_tackles_for_loss","def_tackles_for_loss_yards","def_fumbles_forced","def_sacks","def_sack_yards","def_qb_hits",
    "def_interceptions","def_interception_yards","def_pass_defended","def_tds","def_fumbles","def_safeties", "penalties","penalty_yards"
    ]
team_history_df = team_history_df.select(rel_cols)
print(team_history_df.null_count().glimpse())


player_team_stats = wr_history_df.join(team_history_df, on=["game_id", "team"], how="left")

wr_history_df.write_csv("library/wr_history.csv")
team_history_df.write_csv("library/team_history.csv")
player_team_stats.write_csv("library/player_team_stats.csv")


# features = 
# X = wr_history_df []
# y = wr_history_df ["fantasy_points_ppr"] 

# X_train, X_test,
# y_train, y_test = train_test_split(X, y, random_state=42, test_size= 0.20)

