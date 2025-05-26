from dataclasses import dataclass
from typing import Dict

@dataclass
class TicTacToeConfig:
    board_size: int = 3
    reward_win: int = 1
    reward_draw: int = 0
    reward_lose: int = -1
    reward_illegal_move: int = -1
    action_lookup: Dict[str, str] = None

    def __post_init__(self):
        if self.action_lookup is None:
            # Create a mapping from position names to action indices as strings
            self.action_lookup = {
                "top-left": "0", "top-center": "1", "top-right": "2",
                "middle-left": "3", "center": "4", "middle-right": "5",
                "bottom-left": "6", "bottom-center": "7", "bottom-right": "8"
            }

