# fantasy_analytics
Analytics project for evaluating players in fantasy football

wr_project
# the function is to analyze wr history from the previous year for indicators that lead to a productive fantasy season the next year
# target variable - expected fantasy points/game (weekly)
# predictor variables(?): 
-place on depth chart
-
-target share
-snap count
-red zone targets
-average depth of target (ADOT)
-age and time in the NFL
-Characteristics of QB/Offense (time of possession, pass vs run percent)
-Quality of defense (defensive metrics)

# need to avoid yards, td's, catches? by using variables that are used to calculate fantasy points, we wouldn't be finding anything useful, just that yards/tds/catchs are important to fantasy points

rookie_project

draft_project:
# thoughts: what is an optimal draft strategy depending on size of league, position in draft, randomness of other managers, player scarcity, etc.
putting players into archtypes (touchdown dependent, bellcow rb, big play merchant, etc.)
ex. there aren't 



Core Loading Functions:
    load_pbp() - play-by-play data
    load_player_stats() - player game or season statistics
    load_team_stats() - team game or season statistics
    load_schedules() - game schedules and results
    load_players() - player information
    load_rosters() - team rosters
    load_rosters_weekly() - team rosters by season-week
    load_snap_counts() - snap counts
    load_nextgen_stats() - advanced stats from nextgenstats.nfl.com
    load_ftn_charting() - charted stats from ftnfantasy.com/data
    load_participation() - participation data (historical)
    load_draft_picks() - nfl draft picks
    load_injuries() - injury statuses and practice participation
    load_contracts() - historical contract data from OTC
    load_officials() - officials for each game
    load_combine() - nfl combine results
    load_depth_charts() - depth charts
    load_trades() - trades
    load_ff_playerids() - ffverse/dynastyprocess player ids
    load_ff_rankings() - fantasypros rankings
    load_ff_opportunity() - expected yards, touchdowns, and fantasy points

Utility Functions:
    clear_cache() - Clear cached data
    get_current_season() - Get current NFL season
    get_current_week() - Get current NFL week
