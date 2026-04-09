import time
import torch
import sys
import os
import keyboard

# Adjust path to find your lerobot_abb src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lerobot_abb import ABBRobot, ABBEGMConfig

def run_teleop():
    # Use 250Hz to match ABB EGM standard timing
    config = ABBEGMConfig(port=6510, fps=250)
    robot = ABBRobot(config)
    
    try:
        print("--- ABB EGM Keyboard Teleop ---")
        print("Controls: 'W/S' (J2), 'A/D' (J1), 'Q/E' (J3)")
        print("Press 'ESC' to stop.")
        
        robot.connect()
        
        # Handshake: Wait for initial robot joints
        obs = robot.get_observation()
        while torch.all(obs["qpos"] == 0):
            obs = robot.get_observation()
            time.sleep(0.1)

        current_target = obs["qpos"].clone()
        step_size = 0.3  # Degrees per update for smooth motion
        
        while not keyboard.is_pressed('esc'):
            # J1 - Base
            if keyboard.is_pressed('a'): current_target[0] += step_size
            if keyboard.is_pressed('d'): current_target[0] -= step_size
            
            # J2 - Shoulder
            if keyboard.is_pressed('w'): current_target[1] += step_size
            if keyboard.is_pressed('s'): current_target[1] -= step_size
            
            # J3 - Elbow
            if keyboard.is_pressed('q'): current_target[2] += step_size
            if keyboard.is_pressed('e'): current_target[2] -= step_size

            robot.send_action(current_target)
            
            # 60Hz polling is plenty for human keyboard input
            time.sleep(0.001)

    except Exception as e:
        print(f"Teleop Error: {e}")
    finally:
        robot.disconnect()
        print("Teleop session ended.")

if __name__ == "__main__":
    run_teleop()