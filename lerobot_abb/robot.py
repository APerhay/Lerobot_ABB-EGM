import torch
import time
from threading import Thread, Event
from ABBRobotEGM import EGM
from lerobot.robots.robot import Robot
from .config import ABBEGMConfig

class ABBRobot(Robot):
    def __init__(self, config: ABBEGMConfig):
        super().__init__(config)
        self.config = config
        self.egm = None
        self._stop_event = Event()
        self._thread = None
        self._last_observations = None
        self._next_action = None

    # --- ADD THIS METHOD TO FIX THE ERROR ---
    def configure(self):
        """Required by LeRobot base class. 
        EGM settings are already loaded via self.config.
        """
        pass 
    # -----------------------------------------

    def connect(self):
        self.egm = EGM(port=self.config.port)
        self._stop_event.clear()
        self._thread = Thread(target=self._communication_loop, daemon=True)
        self._thread.start()
        print(f"ABB EGM Server active on port {self.config.port}")

    def _communication_loop(self):
        try:
            while not self._stop_event.is_set():
                success, state = self.egm.receive_from_robot(timeout=1.0)
                if success:
                    self._last_observations = torch.tensor(state.joint_angles.copy(), dtype=torch.float32)
                    cmd = self._next_action.cpu().numpy().tolist() if self._next_action is not None else state.joint_angles.copy()
                    self.egm.send_to_robot(cmd)
                else:
                    time.sleep(0.001)
        except Exception as e:
            print(f"EGM Thread Error: {e}")
        finally:
            if self.egm:
                self.egm.close()

    def get_observation(self) -> dict[str, torch.Tensor]:
        return {"qpos": self._last_observations if self._last_observations is not None else torch.zeros(6)}

    def send_action(self, action: torch.Tensor):
        self._next_action = action

    def disconnect(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        print("ABB Connection Closed.")

    @property
    def name(self) -> str: return "abb_egm"
    @property
    def is_connected(self) -> bool: return self.egm is not None
    @property
    def is_calibrated(self) -> bool: return True
    def calibrate(self): pass
    @property
    def observation_features(self) -> dict: return {"qpos": {"shape": (6,), "dtype": "float32"}}
    @property
    def action_features(self) -> dict: return {"action": {"shape": (6,), "dtype": "float32"}}