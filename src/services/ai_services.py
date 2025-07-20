from typing import Annotated

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from langchain.tools import StructuredTool
from nba_api.stats.endpoints.leaguedashplayerstats import LeagueDashPlayerStats


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
