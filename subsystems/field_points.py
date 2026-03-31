# field_points.py
from wpimath.geometry import Translation2d
import wpilib
from constants import Constants

class FieldPoints:
    @staticmethod
    def getHubPosition() -> Translation2d:
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
            return Constants.FieldConstants.Red.kHubPosition
        return Constants.FieldConstants.Blue.kHubPosition

    @staticmethod
    def getDepotShuttle() -> Translation2d:
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
            return Constants.FieldConstants.Red.kShuttleDepot
        return Constants.FieldConstants.Blue.kShuttleDepot

    @staticmethod
    def getShuttleOutpost() -> Translation2d:
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
            return Constants.FieldConstants.Red.kShuttleOutpost
        return Constants.FieldConstants.Blue.kShuttleOutpost