import wpilib
from robot_container import RobotContainer


class Robot(wpilib.TimedRobot):

    def robotInit(self):
        self.container = RobotContainer()

    def teleopInit(self):
        self.container.teleopInit()

    def robotPeriodic(self):
        self.container.robotPeriodic()


if __name__ == "__main__":
    wpilib.run(Robot)