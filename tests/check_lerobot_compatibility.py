import sys
import os
import torch

# Ensure the src directory is visible


try:
    from lerobot_abb import ABBRobot, ABBEGMConfig
    
    # 1. Test Configuration
    config = ABBEGMConfig(port=6510, fps=250)
    robot = ABBRobot(config)
    
    print("--- LeRobot Compatibility Report ---")
    
    # 2. Check Name
    print(f"Robot Name: {robot.name}")
    
    # 3. Check Observation Shape (CRITICAL for LeRobot Record)
    obs_shape = robot.observation_features['qpos']['shape']
    print(f"Observation Shape: {obs_shape}")
    
    # 4. Check Action Shape (CRITICAL for Teleop)
    act_shape = robot.action_features['action']['shape']
    print(f"Action Shape:      {act_shape}")
    
    # 5. Logical Verification
    if obs_shape == (6,) and act_shape == (6,):
        print("\nSUCCESS: Robot matches ABB 6-DOF configuration.")
        print("Your code is ready for 'lerobot-record'.")
    else:
        print("\nERROR: Shape mismatch. Expected (6,).")

except ImportError as e:
    print(f"Import Error: {e}. Check your folder structure.")
except Exception as e:
    print(f"Unexpected Error: {e}")