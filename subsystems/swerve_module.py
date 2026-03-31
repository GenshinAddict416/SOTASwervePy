import math
from typing import Optional

# WPILib imports
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState, SwerveModulePosition

# REV (Turning Motor - Neo 550) 
# Note: Using SparkMaxConfig for the new 2025/2026 API structure
from rev import SparkMax, SparkLowLevel, SparkMaxConfig
from rev import SparkBase
from rev import SparkBaseConfig
from rev import ResetMode
from rev import PersistMode

# CTRE (Drive Motor - Kraken)
from phoenix6.hardware import TalonFX
from phoenix6.configs import TalonFXConfiguration
from phoenix6.controls import VelocityVoltage
from phoenix6.signals import NeutralModeValue

class SwerveModule:
    def __init__(self, driveCAN: int, turnCAN: int, chassisAngularOffset: float):
        self.chassisOffset = chassisAngularOffset
        
        # --- Physical Constants (Hard-coded from your request) ---
        self.kWheelCircumference = 0.0762 * math.pi
        self.kDriveReduction = (45.0 * 20) / (15 * 15) # 4.0:1

        # --------------------
        # Driving motor (Kraken X60)
        # --------------------
        self.driveMotor = TalonFX(driveCAN)
        
        # Hard-coded Kraken Configuration
        drive_cfg = TalonFXConfiguration()
        drive_cfg.slot0.k_p = 0.1 # Placeholder: Adjust via Constants.DriveConstants.kDrivingP
        drive_cfg.slot0.k_i = 0.0
        drive_cfg.slot0.k_d = 0.0
        drive_cfg.slot0.k_v = 0.12 # Typical for Kraken
        drive_cfg.motor_output.neutral_mode = NeutralModeValue.BRAKE
        drive_cfg.current_limits.supply_current_limit = 50
        drive_cfg.current_limits.supply_current_limit_enable = True
        
        self.driveMotor.configurator.apply(drive_cfg)
        self.driveMotor.set_position(0)
        self.driveVelocityRequest = VelocityVoltage(0.0).with_slot(0)

        # --------------------
        # Turning motor (Neo 550 via SparkMax)
        # --------------------
        self.turnMotor = SparkMax(turnCAN, SparkLowLevel.MotorType.kBrushless)
        self.turnEncoder = self.turnMotor.getAbsoluteEncoder()
        self.turnClosedLoop = self.turnMotor.getClosedLoopController()

        # Hard-coded Turning Configuration (2026 API Pattern)
        turn_cfg = SparkMaxConfig()
        
        # Idle mode and Limits
        turn_cfg.setIdleMode(SparkMaxConfig.IdleMode.kBrake)
        turn_cfg.smartCurrentLimit(20)

        # Encoder - Set to Radians
        turn_cfg.absoluteEncoder.inverted(True)
        turn_cfg.absoluteEncoder.positionConversionFactor(2 * math.pi) # Radians
        turn_cfg.absoluteEncoder.velocityConversionFactor((2 * math.pi) / 60.0)

        # Closed Loop
        turn_cfg.closedLoop.P(1.0)
        turn_cfg.closedLoop.I(0.0)
        turn_cfg.closedLoop.D(0.0)
        turn_cfg.closedLoop.outputRange(-1.0, 1.0)
        
        # Position Wrapping (Continuous motion)
        turn_cfg.closedLoop.positionWrappingEnabled(True)
        turn_cfg.closedLoop.positionWrappingInputRange(0, 2 * math.pi)

        # Apply to hardware
        self.turnMotor.configure(
            turn_cfg, 
            ResetMode.kResetSafeParameters, 
            PersistMode.kPersistParameters
        )

        # --------------------
        # State tracking
        # --------------------
        self.desiredState = SwerveModuleState(0.0, Rotation2d(self.turnEncoder.getPosition()))

    def getState(self) -> SwerveModuleState:
        angle = Rotation2d(self.turnEncoder.getPosition() - self.chassisOffset)
        # Motor RPS -> Wheel RPS -> MPS
        speed = (self.driveMotor.get_velocity().value_as_double / self.kDriveReduction) * self.kWheelCircumference
        return SwerveModuleState(speed, angle)

    def getPosition(self) -> SwerveModulePosition:
        angle = Rotation2d(self.turnEncoder.getPosition() - self.chassisOffset)
        # Motor Rotations -> Wheel Rotations -> Meters
        pos = (self.driveMotor.get_position().value_as_double / self.kDriveReduction) * self.kWheelCircumference
        return SwerveModulePosition(pos, angle)

    def setDesiredState(self, desiredState: SwerveModuleState):
        # Apply chassis offset
        correctedState = SwerveModuleState(
            desiredState.speed,
            desiredState.angle + Rotation2d(self.chassisOffset)
        )

        # Optimize movement
        currentAngle = Rotation2d(self.turnEncoder.getPosition())
        correctedState.optimize(currentAngle)

        # Drive (Kraken) - Command in Rotations Per Second (RPS)
        # MPS -> Wheel RPS -> Motor RPS
        drive_rps = (correctedState.speed / self.kWheelCircumference) * self.kDriveReduction
        self.driveMotor.set_control(self.driveVelocityRequest.with_velocity(drive_rps))

        # Turn (SparkMax) - Command in Radians
        self.turnClosedLoop.setReference(
            correctedState.angle.radians(),
            SparkMax.ControlType.kPosition
        )

        self.desiredState = desiredState

    def resetEncoders(self):
        self.driveMotor.set_position(0)