# Run this file on the command line using 
# >>>python .\BasicEnvironment\GameRunner.py

from BasicEnvironment import *

env = BasicEnv()
env.render()
action = int(input("Enter action:"))
state, reward, done, info = env.step(action)
while not done:
    env.render()
    action = int(input("Enter action:"))
    state, reward, done, info = env.step(action)