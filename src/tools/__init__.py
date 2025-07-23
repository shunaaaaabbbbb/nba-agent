from langchain_core.tools import StructuredTool

from src.tools.call_player_all_seasons import calling_player_all_seasons_tool
from src.tools.call_player_one_season import calling_player_one_season_tool
from src.tools.get_player_id_tool import get_player_id_tool
from src.tools.plot_stats_trend_tool import plot_stats_trend_tool

TOOLS = [
    StructuredTool.from_function(
        calling_player_one_season_tool,
        description="Get NBA stats for a specific player in a specific season. Use this when asked about a player's performance in a particular season.",  # noqa: E501
    ),
    StructuredTool.from_function(
        calling_player_all_seasons_tool,
        description="Get NBA career stats for all seasons for a player by player ID. Use this when asked about a player's career statistics or trends over multiple seasons.",  # noqa: E501
    ),
    StructuredTool.from_function(
        get_player_id_tool,
        description="Get NBA player ID by player name. Use this when you need to convert a player name to their ID for other tools.",  # noqa: E501
    ),
    StructuredTool.from_function(
        plot_stats_trend_tool,
        description="Create a line chart showing the trend of a player's specific stat over multiple seasons. Use this when asked to visualize or show trends in a player's performance over time.",  # noqa: E501
    ),
]
