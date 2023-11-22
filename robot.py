import math
import numpy as np

class Robot:
    def __init__(self, max_motor_speed, wheelbase, lenght, position, rotation):
        self.max_motor_speed = max_motor_speed
        self.wheelbase = wheelbase
        self.lenght = lenght
        self.position = position
        self.rotation = rotation

    
    def draw(self, graphic_engine):
        # draw breadboard
        graphic_engine.draw_rectangle(
            self.position, 
            np.array([0.03, 0.06]), 
            self.rotation,
            (64, 255, 64)
        )

        # draw right wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0] + self.wheelbase * np.cos(np.deg2rad(self.rotation)),
                self.position[1] + self.wheelbase * np.sin(np.deg2rad(-self.rotation))]), 
            np.array([0.02, 0.03]), 
            self.rotation,
            (255, 0, 0)
        )

        # draw left wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0] - self.wheelbase * np.cos(np.deg2rad(self.rotation)),
                self.position[1] - self.wheelbase * np.sin(np.deg2rad(-self.rotation))]), 
            np.array([0.02, 0.03]), 
            self.rotation,
            (255, 0, 0)
        )

        # draw sensors
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0] + self.lenght * np.sin(np.deg2rad(self.rotation)),
                self.position[1] + self.lenght * np.cos(np.deg2rad(-self.rotation))]), 
            np.array([0.08, 0.005]), 
            self.rotation,
            (64, 64, 255)
        )
