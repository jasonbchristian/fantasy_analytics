import nflreadpy as nfl
import polars as pl
import pandas as pd

player = "Patrick Mahomes"
year = 2025

def get_rel_cols(pos_list):
    pos = pos_list[0] if isinstance(pos_list, list) else pos_list
    if pos == "QB":
        return [
            "player_id", "player_display_name", "position",	"season", "week", "season_type", "game_id",
            "team", "opponent_team", "completions", "attempts", "passing_yards", "passing_tds", "passing_interceptions",
            "sacks_suffered", "sack_yards_lost", "sack_fumbles", "sack_fumbles_lost", "passing_air_yards", 
            "passing_yards_after_catch", "passing_first_downs", "passing_epa", "passing_cpoe", "passing_2pt_conversions", 
            "pacr", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost", 
            "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions","fantasy_points" ,"fantasy_points_ppr"
        ]

    elif pos in ["WR", "RB", "TE", "FLEX"]:
        return [
            "player_id", "player_display_name", "position",	"season", "week", "season_type", "game_id",
            "team", "opponent_team", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost",
            "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", "receptions", "targets", "receiving_yards",
            "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", "receiving_air_yards", "receiving_yards_after_catch", 
            "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", "racr", "target_share", "air_yards_share", "wopr",
            "fumble_recovery_own", "fumble_recovery_yards_own", "penalties", "penalty_yards", "fantasy_points" ,"fantasy_points_ppr"
        ]
    elif pos == "K":
        return [
            "player_id", "player_display_name", "position",	"season", "week", "season_type", "game_id",
            "team", "opponent_team", "penalties", "penalty_yards", "fg_made", "fg_att", "fg_missed", "fg_blocked",
            "fg_long", "fg_pct", "fg_made_0_19", "fg_made_20_29", "fg_made_30_39", "fg_made_40_49", "fg_made_50_59",
            "fg_made_60_", "fg_missed_0_19", "fg_missed_20_29", "fg_missed_30_39", "fg_missed_40_49", "fg_missed_50_59",
            "fg_missed_60_", "fg_made_list", "fg_missed_list", "fg_blocked_list", "fg_made_distance", "fg_missed_distance",
            "fg_blocked_distance", "pat_made", "pat_att", "pat_missed", "pat_blocked", "pat_pct", "gwfg_made", "gwfg_att", 
            "gwfg_missed", "gwfg_blocked", "gwfg_distance", "fantasy_points" ,"fantasy_points_ppr"
        ]
    return []
player_stats = nfl.load_player_stats(seasons=[year])
fantasy_pos = ["WR", "RB", "TE"]
rel_cols = get_rel_cols(fantasy_pos)
target_stats = (
    player_stats.filter(pl.col("position").is_in(fantasy_pos))
    .with_columns(
        game_count = pl.len().over("player_id")
    )
    .filter(pl.col("game_count") >= 10)
    .drop("game_count")
    .select(rel_cols)
    .sort(["team","player_display_name"])
    )
target_stats.write_csv("player_season.csv")
print("Player statistics successfully pulled!")