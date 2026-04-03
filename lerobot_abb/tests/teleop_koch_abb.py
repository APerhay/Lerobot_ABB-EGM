import time
import torch
import sys
import os
from lerobot.robots.motors.dynamixel import DynamixelMotorsBus # Typical for Koch arms

# Path to your src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from lerobot_abb import ABBRobot, ABBEGMConfig

def run_koch_teleop():
    # 1. Setup ABB (Follower)
    abb_config = ABBEGMConfig(port=6510, fps=250)
    abb_robot = ABBRobot(abb_config)
    
    # 2. Setup Koch (Leader) - Adjust 'port' to your USB port (e.g., /dev/ttyUSB0 or COM3)
    # This assumes standard Koch 6-DOF mapping
    leader_bus = DynamixelMotorsBus(port="/dev/ttyUSB0", motors={
        "j1": (1, "xl330-m288"), "j2": (2, "xl330-m288"), "j3": (3, "xl330-m288"),
        "j4": (4, "xl330-m288"), "j5": (5, "xl330-m288"), "j6": (6, "xl330-m288")
    })

    try:
        abb_robot.connect()
        leader_bus.connect()
        print("--- Teleop Active: Koch -> ABB ---")

        while True:
            # Read angles from Koch arm
            leader_obs = leader_bus.read_joints() # Returns dict or tensor depending on version
            
            # Convert leader angles to a 6-element tensor for ABB
            # Note: You may need to multiply by -1 or add offsets here 
            # to match the physical orientation of your ISU robotics lab setup.
            action = torch.tensor([
                leader_obs["j1"], leader_obs["j2"], leader_obs["j3"],
                leader_obs["j4"], leader_obs["j5"], leader_obs["j6"]
            ], dtype=torch.float32)

            # Send to ABB
            abb_robot.send_action(action)
            
            # Sync rate (EGM is 250Hz, but 60-100Hz is standard for human teleop)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        abb_robot.disconnect()
        leader_bus.disconnect()

if __name__ == "__main__":
    run_koch_teleop()