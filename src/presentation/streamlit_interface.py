import asyncio
import os

import streamlit as st
from dotenv import load_dotenv

from src.services.ai_services import LangChainAgentService


class StreamlitInterface:
    """Streamlitインターフェース"""

    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            st.error("OPENAI_API_KEY環境変数が設定されていません")
            st.stop()

        # LangChainエージェントサービスの初期化
        self.agent_service = LangChainAgentService(self.openai_api_key)

    def run(self):
        """Streamlitアプリを実行"""
        st.set_page_config(page_title="NBA AI Agent", page_icon="🏀", layout="wide")

        # ヘッダー
        st.title("🏀 NBA AI Agent")
        st.markdown("NBAについて質問してください。")

        # サイドバー
        with st.sidebar:
            st.header("📊 使用例")
            st.markdown(
                """
            - 2024-25レギュラーシーズンのレブロンジェームズのスタッツを教えて
            - ステフィンカリーのキャリア統計は?
            - ニコラヨキッチの得点推移をグラフで見せて
            """
            )

        # 質問入力
        user_question = st.chat_input(
            "質問を入力してください:",
        )
        if user_question:
            self._process_question(user_question)

        # 履歴表示
        if "chat_history" in st.session_state:
            st.header("📝 質問履歴")
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                with st.expander(f"質問 {i+1}: {question[:50]}..."):
                    st.write(f"**質問:** {question}")
                    st.write(f"**回答:** {answer}")

    def _process_question(self, question: str):
        """質問を処理して回答を表示"""
        with st.spinner("🤖 AIが回答を生成中..."):
            try:
                # 非同期処理を実行
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(self.agent_service.process_query(question))
                loop.close()

                # 回答を表示
                st.success("回答が生成されました!")
                st.markdown("### 🤖 AI回答:")
                st.write(response)

                if "trend_graph" in st.session_state:
                    st.plotly_chart(st.session_state["trend_graph"])

                # 履歴に追加
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append((question, response))

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
                st.info("もう一度お試しください。")
