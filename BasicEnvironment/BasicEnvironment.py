from gym import Env
from gym import spaces
import random
import numpy as np
from IPython.display import clear_output
import os

#
# global constants
#

# game board values
NOTHING = 0
PLAYER = 1
WIN = 2
LOSE = 3

# action values
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

#
# Environment Class
#
class BasicEnv(Env):
    def __init__(self):        
        self.cumulative_reward = 0
        #
        # set the initial state to a flattened 6x6 grid with a randomly placed entry, win, and player
        #
        self.state = [NOTHING] * 36

        self.player_position = random.randrange(0, 36)
        self.win_position = random.randrange(0, 36)
        self.lose_position = random.randrange(0, 36)
        
        # make sure the entry and lose points aren't overlapping eachother
        while self.win_position == self.player_position:
            self.win_position = random.randrange(0, 36)

        while self.lose_position == self.win_position or self.lose_position == self.player_position:
            self.lose_position = random.randrange(0, 36)
            
        self.state[self.player_position] = PLAYER
        self.state[self.win_position] = WIN
        self.state[self.lose_position] = LOSE

        # convert the python array into a numpy array (needed since Gym expects the state to be this way)
        self.state = np.array(self.state, dtype=np.int16)

        # observation space (valid ranges for observations in the state)
        self.observation_space = spaces.Box(0, 3, [36,], dtype=np.int16)

        # valid actions:
        #   0 = up
        #   1 = down
        #   2 = left
        #   3 = right
        self.action_space = spaces.Discrete(4)
        
    def step(self, action):
        # placeholder for debugging information
        info = {}

        # set default values for done, reward, and the player position before taking the action
        done = False
        reward = -0.01
        previous_position = self.player_position

        #
        # take the action by moving the player
        #
        if action == UP:
            if (self.player_position - 6) >= 0:
                self.player_position -= 6

        elif action == DOWN:
            if (self.player_position + 6) < 36:
                self.player_position += 6

        elif action == LEFT:
            if (self.player_position % 6) != 0:
                self.player_position -= 1

        elif action == RIGHT:
            if (self.player_position % 6) != 5:
                self.player_position += 1
        else:
            raise Exception("invalid action")

        # 
        # check for win/lose conditions and set reward
        #
        if self.state[self.player_position] == WIN:
            reward = 1.0
            self.cumulative_reward += reward
            done = True
            clear_screen()
            print(f'Cumulative Reward: {self.cumulative_reward}')
            print('YOU WIN!!!!')

        elif self.state[self.player_position] == LOSE:
            reward = -1.0
            self.cumulative_reward += reward
            done = True
            clear_screen()
            print(f'Cumulative Reward: {self.cumulative_reward}')
            print('YOU LOSE')
            
        #
        # Update the environment state
        #
        if not done:
            # update the player position
            self.state[previous_position] = NOTHING
            self.state[self.player_position] = PLAYER
            
        self.cumulative_reward += reward
        return self.state, reward, done, info
    
    def render(self):
        # visualization can be added here
        pretty_print(self.state, self.cumulative_reward)
    
    def reset(self):
        self.cumulative_reward = 0
        #
        # set the initial state to a flattened 6x6 grid with a randomly placed entry, win, and player
        #
        self.state = [NOTHING] * 36

        self.player_position = random.randrange(0, 36)
        self.win_position = random.randrange(0, 36)
        self.lose_position = random.randrange(0, 36)
        
        # make sure the entry and lose points aren't overlapping eachother
        while self.win_position == self.player_position:
            self.win_position = random.randrange(0, 36)

        while self.lose_position == self.win_position or self.lose_position == self.player_position:
            self.lose_position = random.randrange(0, 36)
            
        self.state[self.player_position] = PLAYER
        self.state[self.win_position] = WIN
        self.state[self.lose_position] = LOSE

        # convert the python array into a numpy array (needed since Gym expects the state to be this way)
        self.state = np.array(self.state, dtype=np.int16)

        return self.state

def pretty_print(state_array, cumulative_reward):
    clear_screen()
    print(f'Cumulative Reward: {cumulative_reward}')
    print()
    for i in range(6):
        for j in range(6):
            print('{:4}'.format(state_array[i*6 + j]), end = "")
        print()
    
def clear_screen():
    clear_output()
    os.system("cls")