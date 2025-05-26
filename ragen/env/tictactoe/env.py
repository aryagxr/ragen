import gym
from gym import spaces
import numpy as np
from ragen.env.base import BaseDiscreteActionEnv
from typing import List
from ragen.env.tictactoe.config import TicTacToeConfig

class TicTacToeEnv(BaseDiscreteActionEnv, gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    def __init__(self, env_config=None):
        super(TicTacToeEnv, self).__init__()
        self.observation_space = spaces.Box(0, 2, shape=(3, 3), dtype=np.int8)
        self.action_space = spaces.Discrete(9)
        self.board = np.zeros((3, 3), dtype=int)
        self.done = False
        self.winner = None
        self.cur_player = 1  # 1 for X, 2 for O
        self.config = env_config if env_config is not None else TicTacToeConfig()


    def reset(self, seed=None, options=None, mode=None):
        super().reset(seed=seed)
        self.board = np.zeros((3, 3), dtype=int)
        self.done = False
        self.winner = None
        self.cur_player = 1
        return self.board, {}
    

    def step(self, action):
        if self.done:
            return self.board, 0, True, {}

        # Convert string action name to index if needed
        if isinstance(action, str):
            if action in self.config.action_lookup:
                action = int(self.config.action_lookup[action])
            else:
                return self.board, -10, True, {"invalid_move": True, "error": "Invalid action name"}

        row = action // 3
        col = action % 3
        
        if self.board[row, col] != 0:
            return self.board, -10, True, {"invalid_move": True}

        self.board[row, col] = self.cur_player

        if self._check_win():
            self.done = True
            self.winner = self.cur_player
            reward = 1 if self.cur_player == 1 else -1
            return self.board, reward, True, {}

        if self._check_draw():
            self.done = True
            return self.board, 0, True, {}

        self.cur_player = 3 - self.cur_player  #switch

        return self.board, 0, False, {}


    def render(self, mode="rgb_array"):
        if mode == "human":
            symbols = {0: " ", 1: "X", 2: "O"}
            print("\n")
            for i in range(3):
                print("|", end=" ")
                for j in range(3):
                    print(symbols[self.board[i, j]], end=" | ")
                print("\n-------------")
            print("\n")
            return None
        elif mode == "rgb_array":
            img = np.ones((300, 300, 3), dtype=np.uint8) * 255

            for i in range(1, 3):
                img[i*100:i*100+2, :] = 0
                img[:, i*100:i*100+2] = 0

            for i in range(3):
                for j in range(3):
                    if self.board[i, j] == 1:  # X
                        img[i*100+20:i*100+80, j*100+20:j*100+80] = [255, 0, 0]
                    elif self.board[i, j] == 2:  # O
                        img[i*100+20:i*100+80, j*100+20:j*100+80] = [0, 0, 255]
            return img
        else:
            return self.render("rgb_array")  # Default to rgb_array mode

    
    def _check_win(self):
        for i in range(3):
            if np.all(self.board[i, :] == self.cur_player):
                return True

        for j in range(3):
            if np.all(self.board[:, j] == self.cur_player):
                return True

        if np.all(np.diag(self.board) == self.cur_player):
            return True
        if np.all(np.diag(np.fliplr(self.board)) == self.cur_player):
            return True
        return False

    def _check_draw(self):
        return 0 not in self.board

    def get_all_actions(self) -> List[int]:
        """Get list of all valid actions (empty positions on the board)."""
        valid_actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:  # if position is empty
                    valid_actions.append(i * 3 + j)
        return valid_actions







