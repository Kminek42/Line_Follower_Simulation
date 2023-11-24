import math
import numpy as np

class Robot:
    def __init__(self, max_motor_speed = 1, wheelbase = 0.12, lenght = 0.15, position = np.array([0, 0]), rotation = 0, sensor_width = 0.06, sensor_n = 8):
        self.max_motor_speed = max_motor_speed
        self.wheelbase = wheelbase
        self.lenght = lenght
        self.position = position
        self.rotation = rotation
        self.sensor_n = sensor_n
        self.sensor_width = sensor_width

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
                self.position[0] + 0.5 * self.wheelbase * np.cos(np.deg2rad(self.rotation)),
                self.position[1] + 0.5 * self.wheelbase * np.sin(np.deg2rad(-self.rotation))]), 
            np.array([0.02, 0.03]), 
            self.rotation,
            (255, 0, 0)
        )

        # draw left wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0] - 0.5 * self.wheelbase * np.cos(np.deg2rad(self.rotation)),
                self.position[1] - 0.5 * self.wheelbase * np.sin(np.deg2rad(-self.rotation))]), 
            np.array([0.02, 0.03]), 
            self.rotation,
            (255, 0, 0)
        )

        # draw sensors
        X = np.linspace(-self.sensor_width / 2, self.sensor_width / 2, self.sensor_n)
        for num in X:
            p = rotate_point_around_center(self.position + np.array([num, self.lenght]), self.position, np.deg2rad(-self.rotation))
            graphic_engine.draw_rectangle(
                p, 
                np.array([0.01, 0.01]), 
                self.rotation,
                (64, 64, 255)
            )

    def move(self, motor_l, motor_r, dt):
        motor_l = np.max([np.min([1, motor_l]), -1])
        motor_r = np.max([np.min([1, motor_r]), -1])

        motor_l *= self.max_motor_speed * dt
        motor_r *= self.max_motor_speed * dt
        alpha = np.arctan((motor_r - motor_l) / self.wheelbase)
        if alpha == 0:
            alpha = 1e-3
        
        l = (motor_r + motor_l) / (2 * np.tan(alpha))

        x2 = self.position[0] - l * np.cos(np.deg2rad(self.rotation))
        y2 = self.position[1] + l * np.sin(np.deg2rad(self.rotation))

        rotation_center = np.array([x2, y2])
        
        self.position = rotate_point_around_center(self.position, rotation_center, alpha)
        self.rotation -= np.rad2deg(alpha)

        return (motor_l + motor_r) / 2

    def get_sensors(self, track):
        output = []
        X = np.linspace(-self.sensor_width / 2, self.sensor_width / 2, self.sensor_n)
        for num in X:
            p = rotate_point_around_center(self.position + np.array([num, self.lenght]), self.position, np.deg2rad(-self.rotation))
            d = track.distance_to_chain(p[0], p[1])
            # output.append(np.max([0, 1 - 50 * p]))
            # output.append(track.distance_to_chain(p[0], p[1]) < (track.line_width / 2))
            output.append(np.min([np.max([0, 1 - (d - track.line_width / 2) / 0.01]), 1]))

        return output
 

def rotate_point_around_center(point, center, angle):
    # Calculate the vector from center to point
    delta = point - center
    
    # Calculate the rotation matrix
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    
    # Perform the rotation on the delta vector
    rotated_delta = np.dot(rotation_matrix, delta)
    
    # Calculate the new position by adding the rotated delta to the center
    rotated_point = rotated_delta + center
    
    return rotated_point