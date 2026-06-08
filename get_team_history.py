import nflreadpy as nfl
import polars as pl

#function that returns history for player/s from a range
def get_team_history(year=2025):
   #function to filter relevant columns to player/s
    # def get_rel_cols(pos_list):
    #     col_dict = {
    #         "QB": [
    #             "player_id", "player_display_name", "position",	"season", "week", "season_type",
    #             "team", "opponent_team", "completions", "attempts", "passing_yards", "passing_tds", "passing_interceptions",
    #             "sacks_suffered", "sack_yards_lost", "sack_fumbles", "sack_fumbles_lost", "passing_air_yards", 
    #             "passing_yards_after_catch", "passing_first_downs", "passing_epa", "passing_cpoe", "passing_2pt_conversions", 
    #             "pacr", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", 
    #             "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions","fantasy_points" ,"fantasy_points_ppr"
    #         ],
    #         "WR": [
    #             "player_id", "player_display_name", "position",	"season", "week", "season_type",
    #             "team", "opponent_team", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost",
    #             "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", "receptions", "targets", "receiving_yards",
    #             "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", "receiving_air_yards", "receiving_yards_after_catch", 
    #             "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", "racr", "target_share", "air_yards_share", "wopr",
    #             "fumble_recovery_own", "fumble_recovery_yards_own", "penalties", "penalty_yards", "fantasy_points" ,"fantasy_points_ppr"
    #         ],
    #         "RB": [
    #             "player_id", "player_display_name", "position",	"season", "week", "season_type",
    #             "team", "opponent_team", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost",
    #             "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", "receptions", "targets", "receiving_yards",
    #             "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", "receiving_air_yards", "receiving_yards_after_catch", 
    #             "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", "racr", "target_share", "air_yards_share", "wopr",
    #             "fumble_recovery_own", "fumble_recovery_yards_own", "penalties", "penalty_yards", "fantasy_points" ,"fantasy_points_ppr"
    #         ],
    #         "TE": [
    #             "player_id", "player_display_name", "position",	"season", "week", "season_type",
    #             "team", "opponent_team", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost",
    #             "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", "receptions", "targets", "receiving_yards",
    #             "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", "receiving_air_yards", "receiving_yards_after_catch", 
    #             "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", "racr", "target_share", "air_yards_share", "wopr",
    #             "fumble_recovery_own", "fumble_recovery_yards_own", "penalties", "penalty_yards", "fantasy_points" ,"fantasy_points_ppr"
    #         ],     
    #         "K":[
    #             "player_id", "player_display_name", "position",	"season", "week", "season_type",
    #             "team", "opponent_team", "penalties", "penalty_yards", "fg_made", "fg_att", "fg_missed", "fg_blocked",
    #             "fg_long", "fg_pct", "fg_made_0_19", "fg_made_20_29", "fg_made_30_39", "fg_made_40_49", "fg_made_50_59",
    #             "fg_made_60_", "fg_missed_0_19", "fg_missed_20_29", "fg_missed_30_39", "fg_missed_40_49", "fg_missed_50_59",
    #             "fg_missed_60_", "fg_made_list", "fg_missed_list", "fg_blocked_list", "fg_made_distance", "fg_missed_distance",
    #             "fg_blocked_distance", "pat_made", "pat_att", "pat_missed", "pat_blocked", "pat_pct", "gwfg_made", "gwfg_att", 
    #             "gwfg_missed", "gwfg_blocked", "gwfg_distance", "fantasy_points" ,"fantasy_points_ppr"
    #         ]
    #     }
    #     ordered_cols = {}
    #     for p in pos_list:
    #         if p in col_dict:
    #             for col in col_dict[p]:
    #                 ordered_cols[col] = None
    #     return list(ordered_cols.keys())
    # rel_cols = get_rel_cols(position)

    #loads history from the range
    history = nfl.load_team_stats(seasons=year)
    if "game_id" not in history.columns:
        history = history.with_columns(
            pl.concat_str([pl.col("season"), pl.lit("_"), pl.col("week"), pl.lit("_"), pl.col("team"), pl.lit("_"), pl.col("opponent_team")])
            .alias("game_id")
        )
    #filters the history for relevant player/s and columns, then sorts
    # player_stats = (
    #     history
    #     .filter(pl.col("player_id").is_in(player_ids))
    #     .select(rel_cols)
    #     .sort(["player_display_name", "week"])
    # )

    print(f"Successfully pulled team statistics for {year}!")
    return history

# res = get_team_history()
# res.write_csv("team_history.csv")