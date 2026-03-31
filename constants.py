# constants.py
import math
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics
from wpimath.trajectory import TrapezoidProfile
from util.InterpolatingTreeMap import InterpolatingDoubleTreeMap  # <-- your class


class Constants:

    class DriveConstants:
        # Max speeds
        kMaxSpeedMetersPerSecond = 5.0
        kMaxAngularSpeed = 2 * math.pi

        # Geometry
        kTrackWidth = 0.7366  # 29 inches → meters
        kWheelBase = 0.7366

        kDriveKinematics = SwerveDrive4Kinematics(
            Translation2d(kWheelBase / 2, kTrackWidth / 2),    # FL
            Translation2d(kWheelBase / 2, -kTrackWidth / 2),   # FR
            Translation2d(-kWheelBase / 2, kTrackWidth / 2),   # BL
            Translation2d(-kWheelBase / 2, -kTrackWidth / 2),  # BR
        )

        # Offsets (IMPORTANT)
        kFrontLeftChassisAngularOffset = -math.pi / 2
        kFrontRightChassisAngularOffset = 0.0
        kBackLeftChassisAngularOffset = math.pi
        kBackRightChassisAngularOffset = math.pi / 2

        # CAN IDs
        kFrontLeftDrivingCanId = 5
        kRearLeftDrivingCanId = 3
        kFrontRightDrivingCanId = 7
        kRearRightDrivingCanId = 1

        kFrontLeftTurningCanId = 6
        kRearLeftTurningCanId = 4
        kFrontRightTurningCanId = 8
        kRearRightTurningCanId = 2

        # Misc
        kGyroReversed = False
        kMovementScale = 1.0

        # PID
        kTurningP = 1.5
        kTurningI = 0.0
        kTurningD = 0.0

        kDrivingP = 0.0025
        kDrivingI = 0.0
        kDrivingD = 0.0
        kDrivingV = 0.0


    class ModuleConstants:
        kDrivingMotorPinionTeeth = 15

        kWheelDiameterMeters = 0.0762
        kWheelCircumferenceMeters = kWheelDiameterMeters * math.pi

        kDrivingMotorReduction = (45.0 * 20) / (kDrivingMotorPinionTeeth * 15)

        kDrivingMotorFreeSpeedRps = 5676 / 60.0

        kDriveWheelFreeSpeedRps = (
            kDrivingMotorFreeSpeedRps * kWheelCircumferenceMeters
        ) / kDrivingMotorReduction


    class OIConstants:
        kDriverControllerPort = 0
        kDriveDeadband = 0.05


    class AutoConstants:
        kMaxSpeedMetersPerSecond = 3.0
        kMaxAccelerationMetersPerSecondSquared = 3.0
        kMaxAngularSpeedRadiansPerSecond = math.pi
        kMaxAngularSpeedRadiansPerSecondSquared = math.pi

        kPXController = 1.0
        kPYController = 1.0
        kPThetaController = 1.0

        kThetaControllerConstraints = TrapezoidProfile.Constraints(
            kMaxAngularSpeedRadiansPerSecond,
            kMaxAngularSpeedRadiansPerSecondSquared
        )


    class FieldConstants:
        # CHANGE THESE TO MATCH YOUR FIELD LAYOUT
        # These are from the 2026 FRC game, replace them
        class Red:
            kHubPosition = Translation2d(11.92, 4.0)
            kShuttleDepot = Translation2d(14.3, 2.0)
            kShuttleOutpost = Translation2d(14.3, 6.0)

        class Blue:
            kHubPosition = Translation2d(4.63, 4.0)
            kShuttleDepot = Translation2d(2.5, 2.0)
            kShuttleOutpost = Translation2d(2.5, 6.0)