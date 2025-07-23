import json
from typing import Annotated

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def plot_stats_trend_tool(
    player_name: Annotated[str, "e.g. LeBron James"],
    stat_type: Annotated[str, "e.g. PTS"],
    stats: Annotated[str, "JSON string of player stats data"],
) -> str:
    """
    Plot the trend of a player's stats over time and return the plot data for Streamlit display.
    """
    try:
        # JSON文字列をDataFrameに変換
        stats_data = json.loads(stats)
        _df = pd.DataFrame(stats_data)

        # データが存在するかチェック
        if stat_type not in _df.columns:
            return f"統計項目 '{stat_type}' が見つかりません。利用可能な項目: {list(_df.columns)}"
        else:
            # グラフを作成
            fig = go.Figure()

            # 折れ線グラフを追加
            fig.add_trace(
                go.Scatter(
                    x=_df["SEASON_ID"],
                    y=_df[stat_type],
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
                xaxis={type: "category"},
            )

            st.session_state["trend_graph"] = fig

            return "グラフが生成できました"

    except json.JSONDecodeError:
        return "データの形式が正しくありません。JSON形式でデータを提供してください。"
    except Exception as e:
        return f"グラフ作成中にエラーが発生しました: {e!s}"
