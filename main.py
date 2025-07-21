#!/usr/bin/env python3
"""
NBA AI Agent - NBAプレイヤーの統計データをAIが分析して回答するアプリケーション
"""

import asyncio

from dotenv import load_dotenv
from src.presentation.cli_interface import CLIInterface


def main():
    """メイン関数"""
    # 環境変数の読み込み
    load_dotenv()

    print("🏀 NBA AI Agent を起動中...")

    try:
        # CLIインターフェースを実行
        asyncio.run(CLIInterface().run())
    except ValueError as e:
        print(f"設定エラー: {e}")
    except KeyboardInterrupt:
        print("\n\nNBA AI Agentを終了します。お疲れ様でした!")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        print("アプリケーションを再起動してください。")


if __name__ == "__main__":
    main()
