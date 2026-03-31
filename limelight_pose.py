# limelight_pose.py

"""
THIS IS FOR LIMELIGHT. IF YOU DO NOT HAVE A LIMELIGHT, YOU CAN IGNORE/DELETE THIS FILE.
IF YOU DELETE IT, MAKE SURE TO REMOVE ALL REFERENCES TO IT IN YOUR OTHER FILES.
"""
from networktables import NetworkTableInstance
from wpimath.geometry import Pose2d, Rotation2d
from typing import Optional
import math

class LimelightPose:
    def __init__(self, name: str = "limelight") -> None:
        # Use the default NT instance
        self.table = NetworkTableInstance.getDefault().getTable(name)

    def getPose(self) -> Optional[Pose2d]:
        """Return a Pose2d from Limelight if valid, else None."""
        arr = self.table.getNumberArray("botpose_wpired", [])
        tv = self.table.getNumber("tv", 0)  # target valid
        if tv < 1.0 or len(arr) < 6:
            return None

        x = arr[0]  # meters
        y = arr[1]  # meters
        yaw = arr[5]  # Limelight uses camera rotation order; WPILib wants rotation2d

        return Pose2d(x, y, Rotation2d(yaw))