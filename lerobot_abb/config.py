from dataclasses import dataclass, field
from lerobot.robots.config import RobotConfig

@dataclass
class ABBEGMConfig(RobotConfig):
    # This string must match what you use in the factory/registry
    type: str = "abb_egm"
    
    # EGM specific settings
    port: int = 6510
    
    # Define your ABB robot's joint names for dataset metadata
    joint_names: list[str] = field(
        default_factory=lambda: ["j1", "j2", "j3", "j4", "j5", "j6"]
    )
    
    # Standard LeRobot frequency for ABB EGM
    fps: int = 250