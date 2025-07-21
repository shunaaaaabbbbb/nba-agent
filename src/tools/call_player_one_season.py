from typing import Annotated

from nba_api.stats.endpoints import LeagueDashPlayerStats


def calling_player_one_season_tool(
    player_name: Annotated[str, "e.g. LeBron James"], season: Annotated[str, "e.g. 2024-25"]
) -> str:
    """
    Get NBA stats for a player by name and season.
    """
    # 全選手のシーズンスタッツを取得
    stats = LeagueDashPlayerStats(season=season, per_mode_detailed="PerGame").get_data_frames()[0]
    # 指定選手名で絞り込み
    player_stats = stats[stats["PLAYER_NAME"].str.lower() == player_name.lower()]
    if player_stats.empty:
        return f"No stats found for {player_name} in {season}."
    return player_stats.to_string(index=False)
