import re
from typing import Annotated

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.tools import StructuredTool
from langchain_openai import ChatOpenAI
from nba_api.stats.endpoints.leaguedashplayerstats import LeagueDashPlayerStats

from ..domain.entities import PlayerStats, Query
from ..domain.services import QueryParserService, QueryValidationService, StatsAnalysisService


class OpenAIQueryParserService(QueryParserService):
    """OpenAIを使用したクエリ解析サービス"""

    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

    async def parse_query(self, query_text: str) -> Query:
        """クエリテキストを解析して構造化されたクエリに変換"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """あなたはNBAクエリ解析の専門家です。
            ユーザーの質問から以下の情報を抽出してください:
            - プレイヤー名
            - シーズン(例:2024-25)
            - 統計タイプ(points, rebounds, assists等)

            JSON形式で返してください:
            {
                "player_name": "プレイヤー名",
                "season": "シーズン",
                "stat_type": "統計タイプ"
            }""",
                ),
                ("human", "{query_text}"),
            ]
        )

        try:
            await self.llm.ainvoke(prompt.format_messages(query_text=query_text))
            # 簡易的なパース(実際の実装ではより堅牢にする)  # noqa: ERA001

            # プレイヤー名を抽出
            player_name = None
            if "レブロン" in query_text or "James" in query_text or "ジェームズ" in query_text:
                player_name = "LeBron James"
            elif "curry" in query_text.lower() or "カリー" in query_text:
                player_name = "Stephen Curry"

            # シーズンを抽出
            season = None
            season_match = re.search(r"(\d{4}-\d{2})", query_text)
            if season_match:
                season = season_match.group(1)

            return Query(text=query_text, player_name=player_name, season=season, stat_type=None)
        except Exception as e:
            print(f"クエリ解析エラー: {e}")
            return Query(text=query_text)


class OpenAIStatsAnalysisService(StatsAnalysisService):
    """OpenAIを使用した統計分析サービス"""

    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, openai_api_key=openai_api_key)

    async def analyze_player_stats(self, stats: PlayerStats) -> str:
        """プレイヤーの統計データを分析して自然言語で説明"""
        prompt = f"""
        以下のNBAプレイヤーの統計データを分析して、分かりやすく説明してください:

        プレイヤー名: {stats.player_name}
        シーズン: {stats.season}
        チーム: {stats.team}
        ポジション: {stats.position}

        統計データ:
        - 試合数: {stats.games_played}
        - 平均得点: {stats.points_per_game:.1f}
        - 平均リバウンド: {stats.rebounds_per_game:.1f}
        - 平均アシスト: {stats.assists_per_game:.1f}
        - 平均スティール: {stats.steals_per_game:.1f}
        - 平均ブロック: {stats.blocks_per_game:.1f}
        - フィールドゴール成功率: {stats.field_goal_percentage:.1f}%
        - 3ポイント成功率: {stats.three_point_percentage:.1f}%
        - フリースロー成功率: {stats.free_throw_percentage:.1f}%
        - 平均出場時間: {stats.minutes_per_game:.1f}分

        日本語で、このプレイヤーの特徴や印象的な点を説明してください。
        """

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return response.content  # noqa: TRY300
        except Exception as e:
            print(f"統計分析エラー: {e}")
            return f"{stats.player_name}の{stats.season}シーズンの統計データを取得しましたが、分析中にエラーが発生しました。"  # noqa: E501

    async def compare_stats(self, stats1: PlayerStats, stats2: PlayerStats) -> str:
        """2つのプレイヤーの統計を比較"""
        prompt = f"""
        以下の2人のNBAプレイヤーの統計を比較して、日本語で説明してください:

        {stats1.player_name} ({stats1.season}):
        - 平均得点: {stats1.points_per_game:.1f}
        - 平均リバウンド: {stats1.rebounds_per_game:.1f}
        - 平均アシスト: {stats1.assists_per_game:.1f}

        {stats2.player_name} ({stats2.season}):
        - 平均得点: {stats2.points_per_game:.1f}
        - 平均リバウンド: {stats2.rebounds_per_game:.1f}
        - 平均アシスト: {stats2.assists_per_game:.1f}

        どちらのプレイヤーが優れているか、それぞれの特徴を説明してください。
        """

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return response.content  # noqa: TRY300
        except Exception as e:
            print(f"統計比較エラー: {e}")
            return "統計比較中にエラーが発生しました。"


class OpenAIQueryValidationService(QueryValidationService):
    """OpenAIを使用したクエリ検証サービス"""

    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

    async def validate_query(self, query: Query) -> bool:
        """クエリが有効かどうかを検証"""
        if not query.player_name:
            return False

        # 基本的な検証
        if len(query.text.strip()) < 5:
            return False

        return True

    async def suggest_corrections(self, query: Query) -> list[str]:
        """クエリの修正提案を生成"""
        suggestions = []

        if not query.player_name:
            suggestions.append("プレイヤー名を指定してください(例:レブロンジェームズ)")

        if not query.season:
            suggestions.append("シーズンを指定してください(例:2024-25)")

        if len(query.text.strip()) < 5:
            suggestions.append("より具体的な質問をしてください")

        if not suggestions:
            suggestions.append("NBAプレイヤーの統計について質問してください")

        return suggestions


class LangChainAgentService:
    """LangChainエージェントサービス"""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self._setup_agent()

    def _setup_agent(self):
        """エージェントをセットアップ"""

        def calling_nba_api_tool(
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

        tools = [StructuredTool.from_function(calling_nba_api_tool)]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはNBAプレイヤーの統計について質問に答えるアシスタントです。日本語で回答してください。",
                ),
                ("user", "{input}"),
                ("ai", "{agent_scratchpad}"),
            ]
        )

        model = init_chat_model("gpt-3.5-turbo", model_provider="openai")

        agent = create_tool_calling_agent(model, tools, prompt)

        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    async def process_query(self, query_text: str) -> str:
        """クエリを処理して回答を返す"""
        try:
            response = self.agent_executor.invoke({"input": query_text})
            return response["output"]
        except Exception as e:
            print(f"エージェント処理エラー: {e}")
            return f"エラーが発生しました: {e}"
