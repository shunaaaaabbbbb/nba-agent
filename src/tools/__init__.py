from langchain_core.tools import StructuredTool

from src.tools.call_player_all_seasons import calling_player_all_seasons_tool
from src.tools.call_player_one_season import calling_player_one_season_tool
from src.tools.get_player_id_tool import get_player_id_tool
from src.tools.plot_multiple_stats_tool import plot_multiple_stats_tool
from src.tools.plot_stats_trend_tool import plot_stats_trend_tool

TOOLS = [
    StructuredTool.from_function(calling_player_one_season_tool),
    StructuredTool.from_function(calling_player_all_seasons_tool),
    StructuredTool.from_function(get_player_id_tool),
    StructuredTool.from_function(plot_stats_trend_tool),
    StructuredTool.from_function(plot_multiple_stats_tool),
]
