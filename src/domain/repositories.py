from abc import ABC, abstractmethod

from .entities import Player, PlayerStats, QueryResult


class PlayerRepository(ABC):
    """プレイヤー情報を取得するリポジトリのインターフェース"""

    @abstractmethod
    async def get_player_by_name(self, name: str) -> Player | None:
        """名前でプレイヤーを検索"""
        pass

    @abstractmethod
    async def get_player_stats(self, player_id: int, season: str) -> PlayerStats | None:
        """プレイヤーの統計データを取得"""
        pass

    @abstractmethod
    async def search_players(self, query: str) -> list[Player]:
        """プレイヤーを検索"""
        pass


class QueryRepository(ABC):
    """クエリ履歴を管理するリポジトリのインターフェース"""

    @abstractmethod
    async def save_query_result(self, result: QueryResult) -> None:
        """クエリ結果を保存"""
        pass

    @abstractmethod
    async def get_recent_queries(self, limit: int = 10) -> list[QueryResult]:
        """最近のクエリ結果を取得"""
        pass
