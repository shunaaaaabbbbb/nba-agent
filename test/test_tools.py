import os
import sys

from src.tools.call_player_all_seasons import calling_player_all_seasons_tool
from src.tools.get_player_id_tool import get_player_id_tool

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

player_name = "LeBron James"
player_id = get_player_id_tool(player_name)
print(player_id)
print(calling_player_all_seasons_tool(player_id))
