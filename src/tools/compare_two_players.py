from typing import Annotated, Any

from openai import OpenAI
from openai.types.responses import ResponseCodeInterpreterToolCall, ResponseOutputItem, ResponseOutputMessage

from src.data.stats_schema import SeasonBox


def compare_two_players_tool(
    stats_df_1: Annotated[
        list[SeasonBox],
        "e.g. [{'SEASON_ID': '2024-25', 'PLAYER_NAME': 'LeBron James', 'G': 82, 'MP': 35.6, 'PTS': 27.1, 'AST': 7.7, 'TRB': 7.5, 'FG_PCT': 0.502}, {'SEASON_ID': '2023-24', 'PLAYER_NAME': 'LeBron James', 'G': 82, 'MP': 35.6, 'PTS': 27.1, 'AST': 7.7, 'TRB': 7.5, 'FG_PCT': 0.502}]",  # noqa: E501
    ],
    stats_df_2: Annotated[
        list[SeasonBox],
        "e.g. [{'SEASON_ID': '2024-25', 'PLAYER_NAME': 'LeBron James', 'G': 82, 'MP': 35.6, 'PTS': 27.1, 'AST': 7.7, 'TRB': 7.5, 'FG_PCT': 0.502}, {'SEASON_ID': '2023-24', 'PLAYER_NAME': 'LeBron James', 'G': 82, 'MP': 35.6, 'PTS': 27.1, 'AST': 7.7, 'TRB': 7.5, 'FG_PCT': 0.502}]",  # noqa: E501
    ],
) -> str:
    """
    Compare two players' stats via some charts or graphs by code inpterpreter of OpenAI.
    """
    client = OpenAI()

    instructions = """
    You are a personal NBA stats tutor. When asked a comparison of two players' stats, 
    make some charts or graphs to compare the stats of the two players. 
    IMPORTANT: 
    1. Use matplotlib or seaborn to create clear, informative visualizations
    2. Save the charts as PNG files using plt.savefig() or similar
    3. Focus on key stats like PTS, REB, AST, FG%, 3P%, FT%, STL, BLK
    4. Use appropriate chart types (bar charts, radar charts, scatter plots, etc.)
    5. Make sure to include proper labels, titles, and legends
    6. Create multiple charts if needed to show different aspects of comparison
    7. Use Japanese labels when possible for better understanding
    """

    resp = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
        instructions=instructions,
        input=f"Compare the stats of the two players: {stats_df_1} and {stats_df_2}",
    )

    outputs = resp.output
    structured_output = structure_responses_output(outputs)

    # 結果を文字列として返す
    result_text = ""

    # テキスト部分を追加
    for text in structured_output["texts"]:
        result_text += text + "\n\n"

    # 生成されたファイル(画像など)を取得
    if structured_output["files"]:
        result_text += "## 生成されたグラフ\n\n"

        for file_info in structured_output["files"]:
            try:
                # ファイルの内容を取得
                file_content = client.files.content(file_info["file_id"])

                # ファイル名から拡張子を判定
                filename = file_info["filename"]
                if filename.endswith((".png", ".jpg", ".jpeg")):
                    # 画像ファイルの場合、base64エンコードして表示用のマークダウンを生成
                    import base64

                    # 画像データをbase64エンコード
                    image_data = base64.b64encode(file_content.content).decode("utf-8")

                    # マークダウン形式で画像を埋め込み
                    result_text += f"![{filename}](data:image/png;base64,{image_data})\n\n"

                elif filename.endswith(".csv"):
                    # CSVファイルの場合、内容をテキストとして追加
                    csv_content = file_content.content.decode("utf-8")
                    result_text += f"### {filename}\n```csv\n{csv_content}\n```\n\n"

                else:
                    # その他のファイル
                    result_text += f"### {filename}\nファイルが生成されました。\n\n"

            except Exception as e:
                result_text += f"ファイル {filename} の取得中にエラーが発生しました: {e}\n\n"

    return result_text


def structure_responses_output(outputs: list[ResponseOutputItem]) -> dict[str, Any]:
    """
    Responses API の output を構造化する。
    テキスト・コード・ファイルを dict で返す。
    """
    results = {
        "texts": [],
        "codes": [],
        "files": [],  # {file_id, filename, container_id}
    }

    for output in outputs:
        if isinstance(output, ResponseOutputMessage):
            for c in output.content:
                if c.type == "output_text" and c.text:
                    results["texts"].append(c.text)

                for ann in c.annotations or []:
                    results["files"].append(
                        {
                            "file_id": ann.file_id,
                            "filename": ann.filename,
                            "container_id": ann.container_id,
                        }
                    )

        elif isinstance(output, ResponseCodeInterpreterToolCall):
            if output.code:
                results["codes"].append(output.code)

        else:
            # 想定外のタイプもログしておく
            results.setdefault("unknown", []).append(str(type(output)))

    return results
