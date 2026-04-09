import time
import torch
import sys
import os

# Adjust path to find lerobot_abb src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lerobot_abb import ABBRobot, ABBEGMConfig

def run_test():
    config = ABBEGMConfig(port=6510, fps=250)
    robot = ABBRobot(config)
    
    try:
        print("--- Starting ABB EGM Handshake Test ---")
        robot.connect()
        
        print("Waiting for robot heartbeat...")
        start_wait = time.time()
        obs = robot.get_observation()
        while torch.all(obs["qpos"] == 0):
            if time.time() - start_wait > 20:
                print("Timeout: No robot data. check RAPID.")
                return
            obs = robot.get_observation()
            time.sleep(0.1)

        initial_qpos = obs["qpos"].clone()
        print(f"Connected! Initial Position: {initial_qpos.tolist()}")
        
        # Run test for 15 seconds
        test_duration = 18
        start_time = time.time()

        while (time.time() - start_time) < test_duration:
            elapsed = time.time() - start_time
            
            # Oscillate Joint 2 (Index 1) +/- 10 degrees
            offset = 10.0 * torch.sin(torch.tensor(2 * torch.pi * 0.2 * elapsed))
            target = initial_qpos.clone()
            target[1] += offset
            
            robot.send_action(target)
            
            if int(elapsed * 10) % 10 == 0:
                print(f"Time: {elapsed:.1f}s | Moving J2 to: {target[1]:.2f}")
            
            time.sleep(0.01)

        print("\nTest finished. Triggering RAPID release...")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        robot.disconnect()
        print("Test Complete.")

if __name__ == "__main__":
    run_test()