from typing import Annotated

from nba_api.stats.static import players


def get_player_id_tool(player_name: Annotated[str, "e.g. LeBron James"]) -> str:
    """
    Get NBA player id by name.
    """
    player_id = players.find_players_by_full_name(player_name)[0]["id"]
    return player_id
