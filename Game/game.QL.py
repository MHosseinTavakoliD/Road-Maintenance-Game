import numpy as np
import pandas as pd
import gym

# Initialization
env = gym.make("SmartMDSSgame") # Call the "SmartMDSS_game" environment from gym with the name "env"
action_size = env.action_space.n # Obtain the size of the action space: how many actions. There are 11 here
"""
    - 0: Plow before 1
    - 1: Plow before 2
    - 2: Plow before 3
    - 3: Salt before 
    - 4: Plow During 1
    - 5: Plow During 2
    - 6: Plow During 3
    - 7: Salt During
    - 8: Plow After 1
    - 9: Plow After 2
    - 10: Plow After 3
    - 11: Salt After
"""
state_size = env.observation_space.n # Obtain the size of the state space: For this version: Just consider the snow depth from 0 to 15 inches, every 1 inch
Table = np.zeros((state_size, action_size)) # Initialize the Q table

print (state_size)
# Hyperparameter
epsilon = 0.9 # Parameter for epsilon-greedy
alpha = 1 # Learning rate
gamma = 0.8 # Decay of rewards



