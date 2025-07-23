import json
from typing import Annotated

from nba_api.stats.endpoints import PlayerCareerStats


def calling_player_all_seasons_tool(
    player_id: Annotated[str, "e.g. 237"],
    stats_type_list: Annotated[list[str], "e.g. ['SEASON_ID', 'PTS', 'REB', 'AST']"],
) -> str:
    """
    Get NBA career totals for regular season stats for a player by player ID.
    """
    # PlayerCareerStatsオブジェクトを作成
    player_stats = PlayerCareerStats(player_id=player_id, per_mode36="PerGame")

    # CareerTotalsRegularSeasonのみを取得
    career_totals = player_stats.get_data_frames()[0]
    # TODO: シーズンIDをどうにかする
    career_totals = career_totals[stats_type_list]

    if career_totals.empty:
        return f"No career totals found for player ID {player_id}."

    # DataFrameを辞書のリストに変換
    stats_list = []
    for _, row in career_totals.iterrows():
        season_data = {}
        for col in career_totals.columns:
            value = row[col]
            # 数値の場合は小数点以下2桁に制限
            if isinstance(value, int | float):
                season_data[col] = round(float(value), 2)
            else:
                season_data[col] = value
        stats_list.append(season_data)

    return json.dumps(stats_list, ensure_ascii=False)
