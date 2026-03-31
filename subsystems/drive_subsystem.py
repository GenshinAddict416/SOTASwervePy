#drive_subsystem.py

import wpilib

import commands2

from typing import List
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import ChassisSpeeds, SwerveDrive4Kinematics
from navx import AHRS
from wpilib import Timer
import math

from constants import Constants
from subsystems.swerve_module import SwerveModule
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition
# from limelight_pose import LimelightPose


class DriveSubsystem(commands2.SubsystemBase):
    def __init__(self) -> None:
        # Modules (Can IDs must match your hardware)
        self.fl = SwerveModule(Constants.DriveConstants.kFrontLeftDrivingCanId, Constants.DriveConstants.kFrontLeftTurningCanId, 0.0)
        self.fr = SwerveModule(Constants.DriveConstants.kFrontRightDrivingCanId, Constants.DriveConstants.kFrontRightTurningCanId, 0.0)
        self.bl = SwerveModule(Constants.DriveConstants.kRearLeftDrivingCanId, Constants.DriveConstants.kRearLeftTurningCanId, 0.0)
        self.br = SwerveModule(Constants.DriveConstants.kRearRightDrivingCanId, Constants.DriveConstants.kRearRightTurningCanId, 0.0)

        self.kinematics = Constants.DriveConstants.kDriveKinematics

        # ONLY FOR LIMELIGHT TEAMS
        # self.limelight = LimelightPose()

        
        self.gyro = AHRS.create_spi()
        self.gyro.zeroYaw()

        
        # self.poseEstimator = SwerveDriveOdometry(
        #     self.kinematics,
        #     self.getRotation(),
        #     self.getModulePositions(),
        #     Pose2d()
        # )

    # -----------------------------------------------------------

    # helpers and stuff
    def getRotation(self) -> Rotation2d:
        """Return the current robot rotation as Rotation2d."""
        return self.gyro.getRotation2d()
        # If the gyro is inv erted, you may need to negate the angle:
        # self.gyro.getRotation2d().unaryMinus()

    def getHeading(self) -> float:
        """Return current heading in degrees."""
        return self.getRotation().degrees()

    def zeroHeading(self) -> None:
        """Zero the gyro yaw."""
        self.gyro.zeroYaw()

    def getModulePositions(self) -> List[SwerveModulePosition]:
        """Return current positions of all modules."""
        return [
            self.fl.getPosition(),
            self.fr.getPosition(),
            self.bl.getPosition(),
            self.br.getPosition()
        ]

    # def getPose(self) -> Pose2d:
    #     """Return estimated robot pose from estimator."""
    #     return self.poseEstimator.getEstimatedPosition()

    # def updateVisionPose(self) -> None:
    #     """Fuse Limelight 4 pose into swerve estimator."""
    #     visionPose = self.limelight.getPose()
    #     if visionPose:
    #         # stdDevs = [x meters, y meters, rotation radians]
    #         self.poseEstimator.addVisionMeasurement(
    #             visionPose,
    #             Timer.getFPGATimestamp(),
    #             [0.05, 0.05, math.radians(2)]
    #         )

    # -----------------------------------------------------------

    # driving
    def drive(self, x: float, y: float, rot: float, fieldRelative: bool = True) -> None:
        """Drive the robot with x, y, rotation inputs (-1 to 1)."""
        # Scale to max speed
        x *= Constants.DriveConstants.kMaxSpeedMetersPerSecond
        y *= Constants.DriveConstants.kMaxSpeedMetersPerSecond
        rot *= Constants.DriveConstants.kMaxAngularSpeed

        # Convert to field-relative speeds if needed
        if fieldRelative:
            speeds = ChassisSpeeds.fromFieldRelativeSpeeds(x, y, rot, self.getRotation())
        else:
            speeds = ChassisSpeeds(x, y, rot)

        # Convert to module states
        states: List[SwerveModuleState] = self.kinematics.toSwerveModuleStates(speeds)

        # Clamp wheel speeds to max
        SwerveDrive4Kinematics.desaturateWheelSpeeds(states, Constants.DriveConstants.kMaxSpeedMetersPerSecond)

        # Command modules
        self.fl.setDesiredState(states[0])
        self.fr.setDesiredState(states[1])
        self.bl.setDesiredState(states[2])
        self.br.setDesiredState(states[3])

    # -----------------------------------------------------------

    # periodic updates (~20ms/50Hz)
    def periodic(self) -> None:
        # """Update the pose estimator with latest module positions."""
        # self.poseEstimator.update(
        #     self.getRotation(), 
        #     self.getModulePositions()
        #     )
        # self.updateVisionPose()
        pass
