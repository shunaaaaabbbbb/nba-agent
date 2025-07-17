from ..domain.entities import QueryResult
from ..domain.repositories import QueryRepository


class MemoryQueryRepository(QueryRepository):
    """メモリベースのクエリリポジトリの実装"""

    def __init__(self):
        self.query_history: list[QueryResult] = []

    async def save_query_result(self, result: QueryResult) -> None:
        """クエリ結果を保存"""
        self.query_history.append(result)
        # 履歴を100件までに制限
        if len(self.query_history) > 100:
            self.query_history = self.query_history[-100:]

    async def get_recent_queries(self, limit: int = 10) -> list[QueryResult]:
        """最近のクエリ結果を取得"""
        return self.query_history[-limit:] if self.query_history else []
