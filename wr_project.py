import nflreadpy as nfl
import polars as pl
import get_depth as gd
import get_player_history as ph
import get_team_history as th
from sqlalchemy import create_engine

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
engine = create_engine('sqlite:///football_db/football.db', echo=False)

#narrows to the team history column
query = """
    SELECT
        season, week, team, season_type,  game_id,  opponent_team, completions, attempts, 
        passing_yards, passing_tds, passing_interceptions, sacks_suffered, sack_yards_lost, 
        sack_fumbles, sack_fumbles_lost, passing_air_yards, passing_yards_after_catch, passing_first_downs, passing_epa, passing_cpoe, 
        carries, rushing_yards, rushing_tds, rushing_fumbles, rushing_fumbles_lost, rushing_first_downs, rushing_epa, 
        receptions, targets, receiving_yards, receiving_tds, receiving_fumbles, receiving_fumbles_lost, receiving_air_yards, 
        receiving_yards_after_catch, receiving_first_downs, receiving_epa, 
        def_tackles_solo, def_tackles_with_assist, def_tackle_assists, def_tackles_for_loss, def_tackles_for_loss_yards, def_fumbles_forced, 
        def_sacks, def_sack_yards, def_qb_hits, 
        def_interceptions, def_interception_yards, def_pass_defended, def_tds, def_fumbles, def_safeties, penalties, penalty_yards
    FROM team_game_data
    """

team_history_df = pl.read_database(query=query, connection=engine.connect())

#joins the team-wide stats during each game for each wr
player_team_stats = wr_history_df.join(team_history_df, on=["game_id", "team"], how="left")

#join the opposing team defense stats during each game for each wr
def_cols = [
    "game_id", "team", "def_tackles_solo","def_tackles_with_assist","def_tackle_assists","def_tackles_for_loss","def_tackles_for_loss_yards","def_fumbles_forced",
    "def_sacks","def_sack_yards","def_qb_hits","def_interceptions","def_interception_yards","def_pass_defended","def_tds","def_fumbles","def_safeties"
]
player_team_opp_stats = player_team_stats.join(team_history_df.select(def_cols), left_on =["game_id", "opponent_team"], right_on = ["game_id", "team"], how="left", suffix ="_opp")
player_team_opp_stats = player_team_opp_stats.drop_nans(subset=["receiving_epa","racr"]).drop_nulls(subset=["receiving_epa","racr"])

wr_history_df.write_csv("library/wr_history.csv")
team_history_df.write_csv("library/team_history.csv")
player_team_stats.write_csv("library/player_team_stats.csv")
player_team_opp_stats.write_csv("library/player_team_opp_stats.csv")

# off_features = ["completions","attempts","passing_yards","passing_tds","passing_interceptions","sacks_suffered",
#     "sack_yards_lost","sack_fumbles","sack_fumbles_lost","passing_air_yards","passing_yards_after_catch","passing_first_downs","passing_epa","passing_cpoe","carries_right",
#     "rushing_yards_right","rushing_tds_right","rushing_fumbles_right","rushing_fumbles_lost_right","rushing_first_downs_right"

# ]
# def_features = [
#     "def_tackles_solo","def_tackles_with_assist","def_tackle_assists","def_tackles_for_loss","def_tackles_for_loss_yards","def_fumbles_forced","def_sacks",
#     "def_sack_yards","def_qb_hits","def_interceptions","def_interception_yards", "def_pass_defended", "def_tds","def_fumbles","def_safeties"
# ]
# opp_def_features = [
#     "def_tackles_solo_opp","def_tackles_with_assist_opp","def_tackle_assists_opp","def_tackles_for_loss_opp", "def_tackles_for_loss_yards_opp", "def_fumbles_forced_opp",
#     "def_sacks_opp","def_sack_yards_opp","def_qb_hits_opp","def_interceptions_opp","def_interception_yards_opp","def_pass_defended_opp", "def_tds_opp","def_fumbles_opp","def_safeties_opp"
# ]

features = [
    "receiving_epa","racr","target_share","air_yards_share","wopr", "passing_epa","passing_cpoe", "rushing_epa_right"
]
X = player_team_opp_stats.select(features)

y = player_team_opp_stats.select("fantasy_points_ppr")
