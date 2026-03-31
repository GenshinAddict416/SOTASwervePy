# configs.py

from phoenix6.configs import TalonFXConfiguration
from phoenix6.signals import NeutralModeValue

from rev import SparkMax

from constants import Constants


class ModuleConfigConstants:
    kKrakenFreeSpeedRps = 6000 / 60
    kWheelDiameterMeters = 0.0762
    kWheelCircumferenceMeters = kWheelDiameterMeters * 3.14159265359
    kDrivingMotorPinionTeeth = 15
    kDrivingMotorReduction = (45.0 * 20) / (kDrivingMotorPinionTeeth * 15)
    kDriveWheelFreeSpeedRps = (
        kKrakenFreeSpeedRps * kWheelCircumferenceMeters
    ) / kDrivingMotorReduction


class SwerveModuleConfigs:

    @staticmethod
    def getDrivingConfig() -> TalonFXConfiguration:
        config = TalonFXConfiguration()

        # PID + Feedforward
        config.slot0.kP = Constants.DriveConstants.kDrivingP
        config.slot0.kI = Constants.DriveConstants.kDrivingI
        config.slot0.kD = Constants.DriveConstants.kDrivingD
        config.slot0.kV = Constants.DriveConstants.kDrivingV 

        # Motor behavior
        config.motor_output.neutral_mode = NeutralModeValue.BRAKE

        # Current limiting
        config.current_limits.supply_current_limit = 50
        config.current_limits.supply_current_limit_enable = True

        return config

    # Turning SPARK MAX config (dict for rapid dev 👍)
    turningConfig = {
        "idleMode": SparkMax.IdleMode.kBrake,
        "smartCurrentLimit": 20,
        "absoluteEncoder": {
            "inverted": True,
            "positionConversionFactor": 2 * 3.14159265359,
            "velocityConversionFactor": 2 * 3.14159265359 / 60.0,
        },
        "closedLoop": {
            "pid": {"p": 1, "i": 0, "d": 0},
            "outputRange": (-1, 1),
            "positionWrappingEnabled": True,
            "positionWrappingInputRange": (0, 2 * 3.14159265359),
        },
    }