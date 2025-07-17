from abc import ABC, abstractmethod

from .entities import PlayerStats, Query


class QueryParserService(ABC):
    """クエリ解析サービスのインターフェース"""

    @abstractmethod
    async def parse_query(self, query_text: str) -> Query:
        """クエリテキストを解析して構造化されたクエリに変換"""
        pass


class StatsAnalysisService(ABC):
    """統計分析サービスのインターフェース"""

    @abstractmethod
    async def analyze_player_stats(self, stats: PlayerStats) -> str:
        """プレイヤーの統計データを分析して自然言語で説明"""
        pass

    @abstractmethod
    async def compare_stats(self, stats1: PlayerStats, stats2: PlayerStats) -> str:
        """2つのプレイヤーの統計を比較"""
        pass


class QueryValidationService(ABC):
    """クエリ検証サービスのインターフェース"""

    @abstractmethod
    async def validate_query(self, query: Query) -> bool:
        """クエリが有効かどうかを検証"""
        pass

    @abstractmethod
    async def suggest_corrections(self, query: Query) -> list[str]:
        """クエリの修正提案を生成"""
        pass
