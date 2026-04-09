import sys
import os
import torch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lerobot_abb import ABBRobot, ABBEGMConfig

config = ABBEGMConfig(port=6510, fps=250)

try:
    # Test instantiation
    robot = ABBRobot(config)
    print(f"LeRobot recognized: {robot.name}")
    
    # Test feature mapping
    print(f"Observations: {robot.observation_features}")
    print(f"Actions: {robot.action_features}")
    
except Exception as e:
    print(f"Error: {e}")