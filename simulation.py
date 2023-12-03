import numpy as np
from track import Track
from robot import Robot
from robot_controller import RobotController

class Simulation:
    def __init__(self, controller: RobotController, robot: Robot, track: Track, dt: float):
        self.controller = controller
        self.robot = robot
        self.track = track
        self.dt = dt

    def get_score(self, simulation_time: float):
        self.robot.position = [0, 0]

        s = 0
        for _ in range(int(simulation_time / self.dt)):
            inputs = self.robot.get_sensors(self.track)
            l, r = self.controller.get_motors(inputs)
            s += self.robot.move(l, r, self.dt)

            if self.track.distance_to_chain(self.robot.position[0], self.robot.position[1]) > 0.15:
                return -1e5
            
            if self.robot.rotation > 135 or self.robot.rotation < -135:
                return -1e5
            
        return s
