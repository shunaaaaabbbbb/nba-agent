import asyncio
import os

from ..services.ai_services import LangChainAgentService


class CLIInterface:
    """コマンドラインインターフェース"""

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY環境変数が設定されていません")

        # LangChainエージェントサービスの初期化
        self.agent_service = LangChainAgentService(self.openai_api_key)

    async def run(self):
        """CLIを実行"""
        print("🏀 NBA AI Agent へようこそ!")
        print("NBAプレイヤーの統計について質問してください。")
        print("例: 2024-25レギュラーシーズンのレブロンジェームズのスタッツを教えて")
        print("終了するには 'quit' または 'exit' と入力してください。")
        print("-" * 50)

        while True:
            try:
                user_input = input("\n質問を入力してください: ").strip()

                if user_input.lower() in ["quit", "exit", "終了"]:
                    print("NBA AI Agentを終了します。お疲れ様でした!")
                    break

                if not user_input:
                    continue

                # エージェントでクエリを処理
                print("\n🤖 AI回答:")
                response = await self.agent_service.process_query(user_input)
                print(response)

            except KeyboardInterrupt:
                print("\n\nNBA AI Agentを終了します。お疲れ様でした!")
                break
            except Exception as e:
                print(f"\n❌ エラーが発生しました: {e}")
                print("もう一度お試しください。")


async def main():
    """メイン関数"""
    try:
        cli = CLIInterface()
        await cli.run()
    except ValueError as e:
        print(f"設定エラー: {e}")
        print("OPENAI_API_KEY環境変数を設定してください。")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    asyncio.run(main())
