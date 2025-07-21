from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

from src.tools import TOOLS


class LangChainAgentService:
    """LangChainエージェントサービス"""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self._setup_agent()

    def _setup_agent(self):
        """エージェントをセットアップ"""
        tools = TOOLS

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
