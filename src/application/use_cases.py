from datetime import datetime

from ..domain.entities import Player, QueryResult
from ..domain.repositories import PlayerRepository, QueryRepository
from ..domain.services import QueryParserService, QueryValidationService, StatsAnalysisService


class GetPlayerStatsUseCase:
    """プレイヤーの統計データを取得するユースケース"""

    def __init__(
        self,
        player_repository: PlayerRepository,
        query_repository: QueryRepository,
        query_parser: QueryParserService,
        stats_analyzer: StatsAnalysisService,
        query_validator: QueryValidationService,
    ):
        self.player_repository = player_repository
        self.query_repository = query_repository
        self.query_parser = query_parser
        self.stats_analyzer = stats_analyzer
        self.query_validator = query_validator

    async def execute(self, query_text: str) -> QueryResult:
        """クエリを実行して結果を返す"""
        # クエリを解析
        query = await self.query_parser.parse_query(query_text)

        # クエリを検証
        if not await self.query_validator.validate_query(query):
            corrections = await self.query_validator.suggest_corrections(query)
            return QueryResult(
                query=query,
                answer=f"クエリが無効です。修正案: {', '.join(corrections)}",
                data_source="validation",
                timestamp=datetime.now(),
            )

        # プレイヤーを検索
        if query.player_name:
            player = await self.player_repository.get_player_by_name(query.player_name)
            if not player:
                return QueryResult(
                    query=query,
                    answer=f"プレイヤー '{query.player_name}' が見つかりませんでした。",
                    data_source="player_search",
                    timestamp=datetime.now(),
                )

            # 統計データを取得
            season = query.season or "2024-25"
            stats = await self.player_repository.get_player_stats(player.id, season)

            if not stats:
                return QueryResult(
                    query=query,
                    answer=f"{player.name}の{season}シーズンの統計データが見つかりませんでした。",
                    data_source="stats_search",
                    timestamp=datetime.now(),
                )

            # 統計データを分析
            analysis = await self.stats_analyzer.analyze_player_stats(stats)

            result = QueryResult(query=query, answer=analysis, data_source="nba_api", timestamp=datetime.now())

            # 結果を保存
            await self.query_repository.save_query_result(result)

            return result

        return QueryResult(
            query=query,
            answer="プレイヤー名が指定されていません。",
            data_source="validation",
            timestamp=datetime.now(),
        )


class SearchPlayersUseCase:
    """プレイヤーを検索するユースケース"""

    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository

    async def execute(self, search_query: str) -> list[Player]:
        """プレイヤーを検索して結果を返す"""
        return await self.player_repository.search_players(search_query)


class GetQueryHistoryUseCase:
    """クエリ履歴を取得するユースケース"""

    def __init__(self, query_repository: QueryRepository):
        self.query_repository = query_repository

    async def execute(self, limit: int = 10) -> list[QueryResult]:
        """最近のクエリ履歴を取得"""
        return await self.query_repository.get_recent_queries(limit)
