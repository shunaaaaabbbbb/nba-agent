import json
import os
from datetime import datetime
from typing import Annotated

import pandas as pd
import plotly.graph_objects as go


def plot_stats_trend_tool(
    player_name: Annotated[str, "e.g. LeBron James"],
    stat_type: Annotated[str, "e.g. PTS"],
    stats_df: Annotated[str, "JSON string of player stats data"],
) -> str:
    """
    Plot the trend of a player's stats over time. 折れ線グラフを作成してファイルに保存する
    """
    try:
        # JSON文字列をDataFrameに変換
        stats_data = json.loads(stats_df)
        stats_df = pd.DataFrame(stats_data)

        # グラフを作成
        fig = go.Figure()

        # データが存在するかチェック
        if stat_type not in stats_df.columns:
            return f"統計項目 '{stat_type}' が見つかりません。利用可能な項目: {list(stats_df.columns)}"

        # 折れ線グラフを追加
        fig.add_trace(
            go.Scatter(
                x=stats_df["SEASON_ID"],
                y=stats_df[stat_type],
                mode="lines+markers",
                name=stat_type,
                line={"color": "blue", "width": 2},
                marker={"size": 6},
            )
        )

        # レイアウトを設定
        fig.update_layout(
            title=f"{player_name}の{stat_type}推移",
            xaxis_title="シーズン",
            yaxis_title=stat_type,
            template="plotly_white",
            height=500,
        )

        safe_player_name = "".join(c for c in player_name if c.isalnum() or c in (" ", "-")).rstrip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_player_name}_{stat_type}_{timestamp}.html"

        # 保存ディレクトリを作成
        output_dir = "graphs"
        os.makedirs(output_dir, exist_ok=True)

        # ファイルパスを生成
        filepath = os.path.join(output_dir, filename)

        # HTMLファイルとして保存
        fig.write_html(filepath, include_plotlyjs=True)

        return f"グラフを保存しました: {filepath}"  # noqa: TRY300

    except json.JSONDecodeError:
        return "データの形式が正しくありません。JSON形式でデータを提供してください。"
    except Exception as e:
        return f"グラフ作成中にエラーが発生しました: {e!s}"
