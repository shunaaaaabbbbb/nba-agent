from dataclasses import dataclass
from datetime import datetime


@dataclass
class Player:
    """NBAプレイヤーのエンティティ"""

    id: int
    name: str
    team: str
    position: str | None = None
    height: str | None = None
    weight: str | None = None
    birth_date: datetime | None = None


@dataclass
class PlayerStats:
    """プレイヤーの統計データエンティティ"""

    player_id: int
    player_name: str
    season: str
    games_played: int
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    steals_per_game: float
    blocks_per_game: float
    field_goal_percentage: float
    three_point_percentage: float
    free_throw_percentage: float
    minutes_per_game: float
    games_started: int
    total_points: int
    total_rebounds: int
    total_assists: int
    total_steals: int
    total_blocks: int
    team: str
    position: str | None = None


@dataclass
class Query:
    """ユーザークエリのエンティティ"""

    text: str
    player_name: str | None = None
    season: str | None = None
    stat_type: str | None = None


@dataclass
class QueryResult:
    """クエリ結果のエンティティ"""

    query: Query
    answer: str
    data_source: str
    timestamp: datetime
