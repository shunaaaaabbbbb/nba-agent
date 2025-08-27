from typing import Annotated

from nba_api.stats.endpoints import LeagueDashPlayerStats

from src.data.schemas import PlayerStats


def calling_player_one_season_tool(
    player_id: Annotated[int, "e.g. 23745"],
    player_name: Annotated[str, "e.g. LeBron James"],
    season: Annotated[str, "e.g. 2024-25"],
    season_type: Annotated[str, "e.g. Regular Season"],
) -> list[PlayerStats]:
    """
    Get NBA stats for a player by name and season.
    """
    # 全選手の指定シーズンのスタッツを取得
    stats = LeagueDashPlayerStats(
        season=season, per_mode_detailed="PerGame", season_type_all_star=season_type
    ).get_data_frames()[0]
    player_stats = stats[stats["PLAYER_ID"] == player_id]
    if player_stats.empty:
        return f"No stats found for {player_name} in {season}."
    records = player_stats.to_dict(orient="records")

    return [PlayerStats(**record) for record in records]
