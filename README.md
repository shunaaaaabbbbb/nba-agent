# NBA AI Agent

NBAプレイヤーの統計データをAIが分析して回答するアプリケーションです。

## 機能

- 🏀 NBAプレイヤーの統計データ取得
- 🤖 OpenAI GPTを使用した自然言語での回答
- 📊 詳細な統計分析（得点、リバウンド、アシスト等）
- 🔍 プレイヤー検索機能
- 📝 クエリ履歴の保存

## アーキテクチャ

このプロジェクトはクリーンアーキテクチャとドメイン駆動設計の原則に従って構築されています：

```
src/
├── domain/           # ドメイン層（エンティティ、リポジトリインターフェース、ドメインサービス）
├── application/      # アプリケーション層（ユースケース）
├── infrastructure/   # インフラストラクチャ層（NBA API、メモリリポジトリ）
├── services/         # サービス層（AIサービス）
└── presentation/     # プレゼンテーション層（CLIインターフェース）
```

## セットアップ

### 1. 依存関係のインストール

```bash
# uvを使用して依存関係をインストール
uv sync
```

### 2. 環境変数の設定

```bash
# 環境変数ファイルをコピー
cp env.example .env

# .envファイルを編集してOpenAI API Keyを設定
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. OpenAI API Keyの取得

1. [OpenAI Platform](https://platform.openai.com/api-keys) にアクセス
2. アカウントを作成またはログイン
3. API Keyを生成
4. `.env`ファイルに設定

## 使用方法

### 基本的な使用方法

```bash
# アプリケーションを起動
python main.py
```

### 質問例

- "2024-25レギュラーシーズンのレブロンジェームズのスタッツを教えて"
- "ステフィンカリーの得点は？"
- "2023-24シーズンのケビン・デュラントの統計"

## 技術スタック

- **Python 3.11+**
- **LangChain** - AIアプリケーション開発フレームワーク
- **OpenAI GPT** - 自然言語処理
- **NBA API** - NBAデータ取得
- **Pydantic** - データバリデーション
- **asyncio** - 非同期処理

## プロジェクト構造

```
nba-agent/
├── main.py                 # エントリーポイント
├── pyproject.toml         # プロジェクト設定
├── env.example           # 環境変数テンプレート
├── README.md             # このファイル
└── src/
    ├── domain/           # ドメイン層
    │   ├── entities.py   # エンティティ
    │   ├── repositories.py # リポジトリインターフェース
    │   └── services.py   # ドメインサービス
    ├── application/      # アプリケーション層
    │   └── use_cases.py # ユースケース
    ├── infrastructure/   # インフラストラクチャ層
    │   ├── nba_api_repository.py # NBA API実装
    │   └── memory_query_repository.py # メモリリポジトリ
    ├── services/         # サービス層
    │   └── ai_services.py # AIサービス実装
    └── presentation/     # プレゼンテーション層
        └── cli_interface.py # CLIインターフェース
```

## 今後の機能追加予定

- [ ] Web UI（Streamlit/FastAPI）
- [ ] データベース連携（PostgreSQL）
- [ ] チーム統計分析
- [ ] プレイヤー比較機能
- [ ] リアルタイム試合データ
- [ ] 予測分析機能

## ライセンス

MIT License