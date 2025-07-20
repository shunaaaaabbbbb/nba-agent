import json
from typing import Annotated

from nba_api.stats.endpoints import PlayerCareerStats


def calling_player_all_seasons_tool(player_id: Annotated[str, "e.g. 237"]) -> str:
    """
    Get NBA career totals for regular season stats for a player by player ID.
    """
    # PlayerCareerStatsオブジェクトを作成
    player_stats = PlayerCareerStats(player_id=player_id)

    # CareerTotalsRegularSeasonのみを取得
    career_totals = player_stats.get_data_frames()[0]

    if career_totals.empty:
        return f"No career totals found for player ID {player_id}."

    # 必要な列のみを選択してリスト形式のJSONに変換
    selected_columns = ["SEASON_ID", "PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FG3_PCT", "FT_PCT"]
    available_columns = [col for col in selected_columns if col in career_totals.columns]

    # DataFrameを辞書のリストに変換
    stats_list = []
    for _, row in career_totals.iterrows():
        season_data = {}
        for col in available_columns:
            value = row[col]
            # 数値の場合は小数点以下2桁に制限
            if isinstance(value, int | float):
                season_data[col] = round(float(value), 2)
            else:
                season_data[col] = value
        stats_list.append(season_data)

    return json.dumps(stats_list, ensure_ascii=False)
