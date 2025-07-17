import asyncio

from nba_api.stats.endpoints import commonplayerinfo, playercareerstats
from nba_api.stats.static import players

from ..domain.entities import Player, PlayerStats
from ..domain.repositories import PlayerRepository


class NBAApiRepository(PlayerRepository):
    """NBA APIを使用したプレイヤーリポジトリの実装"""

    def __init__(self):
        self.players_cache = {}
        self._load_players_cache()

    def _load_players_cache(self):
        """プレイヤーリストをキャッシュに読み込み"""
        try:
            all_players = players.get_players()
            for player_data in all_players:
                name = player_data.get("full_name", "")
                if name:
                    self.players_cache[name.lower()] = player_data
        except Exception as e:
            print(f"プレイヤーキャッシュの読み込みに失敗: {e}")

    async def get_player_by_name(self, name: str) -> Player | None:
        """名前でプレイヤーを検索"""
        try:
            # キャッシュから検索
            name_lower = name.lower()
            for cached_name, player_data in self.players_cache.items():
                if name_lower in cached_name or cached_name in name_lower:
                    return Player(
                        id=player_data.get("id"),
                        name=player_data.get("full_name", ""),
                        team=player_data.get("team", ""),
                        position=player_data.get("position", ""),
                        height=player_data.get("height", ""),
                        weight=player_data.get("weight", ""),
                    )

            # 直接APIで検索
            loop = asyncio.get_event_loop()
            player_info = await loop.run_in_executor(None, lambda: commonplayerinfo.CommonPlayerInfo(player_name=name))

            if player_info.get_dict()["resultSets"][0]["rowSet"]:
                player_data = player_info.get_dict()["resultSets"][0]["rowSet"][0]
                return Player(
                    id=player_data[0],
                    name=player_data[1],
                    team=player_data[3] if len(player_data) > 3 else "",
                    position=player_data[2] if len(player_data) > 2 else "",
                )

            return None  # noqa: TRY300
        except Exception as e:
            print(f"プレイヤー検索エラー: {e}")
            return None

    async def get_player_stats(self, player_id: int, season: str) -> PlayerStats | None:
        """プレイヤーの統計データを取得"""
        try:
            loop = asyncio.get_event_loop()
            career_stats = await loop.run_in_executor(
                None, lambda: playercareerstats.PlayerCareerStats(player_id=player_id)
            )

            stats_dict = career_stats.get_dict()
            if not stats_dict["resultSets"][0]["rowSet"]:
                return None

            # 最新の統計データを取得
            stats_data = stats_dict["resultSets"][0]["rowSet"][0]

            return PlayerStats(
                player_id=player_id,
                player_name=stats_data[1] if len(stats_data) > 1 else "",
                season=season,
                games_played=stats_data[3] if len(stats_data) > 3 else 0,
                points_per_game=stats_data[26] if len(stats_data) > 26 else 0.0,
                rebounds_per_game=stats_data[20] if len(stats_data) > 20 else 0.0,
                assists_per_game=stats_data[21] if len(stats_data) > 21 else 0.0,
                steals_per_game=stats_data[22] if len(stats_data) > 22 else 0.0,
                blocks_per_game=stats_data[23] if len(stats_data) > 23 else 0.0,
                field_goal_percentage=stats_data[10] if len(stats_data) > 10 else 0.0,
                three_point_percentage=stats_data[13] if len(stats_data) > 13 else 0.0,
                free_throw_percentage=stats_data[16] if len(stats_data) > 16 else 0.0,
                minutes_per_game=stats_data[8] if len(stats_data) > 8 else 0.0,
                games_started=stats_data[4] if len(stats_data) > 4 else 0,
                total_points=stats_data[26] * stats_data[3] if len(stats_data) > 26 else 0,
                total_rebounds=stats_data[20] * stats_data[3] if len(stats_data) > 20 else 0,
                total_assists=stats_data[21] * stats_data[3] if len(stats_data) > 21 else 0,
                total_steals=stats_data[22] * stats_data[3] if len(stats_data) > 22 else 0,
                total_blocks=stats_data[23] * stats_data[3] if len(stats_data) > 23 else 0,
                team=stats_data[2] if len(stats_data) > 2 else "",
                position=stats_data[5] if len(stats_data) > 5 else "",
            )
        except Exception as e:
            print(f"統計データ取得エラー: {e}")
            return None

    async def search_players(self, query: str) -> list[Player]:
        """プレイヤーを検索"""
        try:
            results = []
            query_lower = query.lower()

            for name, player_data in self.players_cache.items():
                if query_lower in name:
                    results.append(
                        Player(
                            id=player_data.get("id"),
                            name=player_data.get("full_name", ""),
                            team=player_data.get("team", ""),
                            position=player_data.get("position", ""),
                        )
                    )

            return results[:10]  # 最大10件まで
        except Exception as e:
            print(f"プレイヤー検索エラー: {e}")
            return []
