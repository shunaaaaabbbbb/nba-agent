from pydantic import BaseModel, Field


class SeasonBox(BaseModel):
    PLAYER_ID: int = Field(ge=0)
    PLAYER_NAME: str
    NICKNAME: str
    TEAM_ID: int = Field(ge=0)
    TEAM_ABBREVIATION: str

    AGE: int = Field(ge=0)
    GP: int = Field(ge=0)
    W: int = Field(ge=0)
    L: int = Field(ge=0)
    W_PCT: float = Field(ge=0, le=1)

    MIN: float = Field(ge=0)

    FGM: float = Field(ge=0)
    FGA: float = Field(ge=0)
    FG_PCT: float = Field(ge=0, le=1)

    FG3M: float = Field(ge=0)
    FG3A: float = Field(ge=0)
    FG3_PCT: float = Field(ge=0, le=1)

    FTM: float = Field(ge=0)
    FTA: float = Field(ge=0)
    FT_PCT: float = Field(ge=0, le=1)

    OREB: float = Field(ge=0)
    DREB: float = Field(ge=0)
    REB: float = Field(ge=0)

    AST: float = Field(ge=0)
    TOV: float = Field(ge=0)
    STL: float = Field(ge=0)
    BLK: float = Field(ge=0)
    BLKA: float = Field(ge=0)
    PF: float = Field(ge=0)
    PFD: float = Field(ge=0)
    PTS: float = Field(ge=0)
    PLUS_MINUS: float
    NBA_FANTASY_PTS: float
    DD2: float = Field(ge=0)
    TD3: float = Field(ge=0)
