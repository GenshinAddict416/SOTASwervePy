# robot_container.py
import wpilib
from wpilib import XboxController
from commands2 import RunCommand, CommandScheduler

from constants import Constants
from subsystems.drive_subsystem import DriveSubsystem


class RobotContainer:
    def __init__(self) -> None:
        # ---------------------------
        # CONTROLLER
        # ---------------------------
        self.driverController = XboxController(0)

        # ---------------------------
        # SUBSYSTEMS
        # ---------------------------
        self.m_drive = DriveSubsystem()

        # ---------------------------
        # DEFAULT COMMANDS
        # ---------------------------
        # Set the swerve drive default to read controller input
        self.m_driveDefault()

    # ---------------------------
    # DEFAULT DRIVETRAIN COMMAND
    # ---------------------------
    def m_driveDefault(self) -> None:
        self.m_drive.setDefaultCommand(
            RunCommand(lambda: self._driveWithController(), self.m_drive)
        )

    def _driveWithController(self) -> None:
        """Read controller sticks and drive the robot."""
        # Get axes (range -1 to 1)
        x = self._applyDeadband(-self.driverController.getLeftY())   # Forward/back
        y = self._applyDeadband(-self.driverController.getLeftX())   # Left/right
        rot = self._applyDeadband(-self.driverController.getRightX())  # Rotation

        # Drive the robot (field-relative)
        self.m_drive.drive(x, y, rot, fieldRelative=True)

    def _applyDeadband(self, value: float) -> float:
        return value if abs(value) > 0.05 else 0.0

    # ---------------------------
    # TELEOP INIT
    # ---------------------------
    def teleopInit(self) -> None:
        """Reset heading and optionally module encoders at start of teleop."""
        self.m_drive.zeroHeading()
        # self.m_drive.resetModules()  # uncomment if you add this helper

    # ---------------------------
    # PERIODIC
    # ---------------------------
    def robotPeriodic(self) -> None:
        """Update pose estimator periodically."""
        self.m_drive.periodic()
        # Run scheduled commands
        CommandScheduler.getInstance().run()