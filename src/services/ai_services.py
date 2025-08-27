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
                    """あなたはNBAプレイヤーの統計について質問に答える専門アシスタントです。以下の重要なルールと知識に従って日本語で回答してください

## NBAシーズンの理解
- 2016年と入力されたら2015-16シーズンとして解釈してください
- 2024年と入力されたら2023-24シーズンとして解釈してください
- シーズンは通常「2023-24」のような形式で表現されます
- 現在のシーズンは2024-25です

## 統計データの理解
- 取得できたデータは特別な指示がない限り全て表示してください

## 回答のガイドライン
1. 統計データは分かりやすく日本語で説明してください
2. 数値は適切に四捨五入して表示してください
3. プレイヤーが見つからない場合は、類似の名前を提案してください
4. キャリア統計を聞かれた場合は、全シーズンのデータを分析してください
5. トレンド分析を求められた場合は、グラフ作成ツールを使用してください
6. 統計の意味や重要性についても説明してください

## 選手名
旧ユーゴスラビアの選手名(...ッチで終わる選手)のcはčやćに変えてください

常に親切で分かりやすい回答を心がけてください。""",
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
