import numpy as np
import matplotlib.pyplot as plt
import track

class Robot:
    def __init__(self, *,
                 max_motor_speed, 
                 wheelbase, 
                 engine_cutoff, 
                 lenght, 
                 position, 
                 rotation, 
                 sensor_width, 
                 sensor_n, 
                 sensor_noise,
                 min_speed,
                 sensor_radius,
                 track_width):

        wheelbase = np.array(wheelbase)
        position = np.array(position)
        lenght = np.array(lenght)
        sensor_width = np.array(sensor_width)

        assert wheelbase.ndim == 1
        assert wheelbase.all() > 0

        assert lenght.ndim == 1
        assert lenght.all() > 0

        assert sensor_width.ndim == 1
        assert sensor_width.all() > 0

        assert position.shape == (2, )

        assert isinstance(max_motor_speed, float)
        assert isinstance(sensor_noise, float)
        assert isinstance(engine_cutoff, float)
        assert isinstance(min_speed, float)
        assert isinstance(sensor_radius, float)
        assert isinstance(track_width, float)

        self.robot_n = wheelbase.shape[0]

        self.position = np.tile(position, (self.robot_n, )).reshape((-1, 2))
        self.rotation = np.array(rotation).repeat(self.robot_n, axis=0)

        self.wheelbase = wheelbase
        self.lenght = lenght

        self.max_motor_speed = max_motor_speed
        self.cutoff = engine_cutoff
        self.min_speed = min_speed

        self.sensor_n = sensor_n
        self.sensor_width = sensor_width
        self.sensor_noise = sensor_noise
        self.sensor_radius = sensor_radius
        self.track_width = track_width

        self.m1_v = 0
        self.m2_v = 0


    def move(self, motor_l, motor_r, dt):
        # limit input
        motor_l = np.clip(motor_l, -1, 1)
        motor_r = np.clip(motor_r, -1, 1)
        
        # apply inertia
        self.m1_v += self.cutoff * (motor_l - self.m1_v)
        self.m2_v += self.cutoff * (motor_r - self.m2_v)

        # apply speed
        motor_l = self.max_motor_speed * self.m1_v
        motor_r = self.max_motor_speed * self.m2_v

        # apply friction
        motor_l[np.abs(motor_l) < self.min_speed] = 0
        motor_r[np.abs(motor_r) < self.min_speed] = 0

        # move robot
        V = (motor_r + motor_l) / 2
        w = (motor_r - motor_l) / self.wheelbase

        translation = np.array([
            np.cos(self.rotation) * V,
            np.sin(self.rotation) * V
        ]).T

        self.position += translation * dt
        self.rotation += w * dt

        return (self.m1_v + self.m2_v) / 2


    def get_sensors(self, track: track.Track):
        # Create vector of sensors of each robot (robot_n * sensor_n), for easy use in the track function
        X = np.linspace(-self.sensor_width / 2, self.sensor_width / 2, self.sensor_n).T.reshape((-1))

        Y = np.repeat(self.lenght, self.sensor_n)

        angle = np.repeat(self.rotation, self.sensor_n)

        x_rotated = X * np.cos(angle) - Y * np.sin(angle)
        y_rotated = X * np.sin(angle) + Y * np.cos(angle)

        positions = np.stack((x_rotated, y_rotated), axis=1)
        print('positions:', positions)
        positions += np.repeat(self.position, self.sensor_n, axis=1).T
        print('new positions:', positions)
        
        readings = track.distance_to_chain(positions)
        readings = (self.sensor_radius + self.track_width / 2 - readings) / self.sensor_radius
        readings = np.clip(readings, 0.0, 1.0)
        readings += self.sensor_noise * np.random.randn(self.robot_n * self.sensor_n)
        readings = np.clip(readings, 0.0, 1.0)

        return readings.reshape(self.robot_n, self.sensor_n)
    
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
                self.position[1] + 0.5 * self.wheelbase * np.sin(np.deg2rad(-self.rotation))]
            ), 
            np.array([0.02, 0.03]), 
            self.rotation,
            (255, 0, 0)
        )

        # draw left wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0] - 0.5 * self.wheelbase * np.cos(np.deg2rad(self.rotation)),
                self.position[1] - 0.5 * self.wheelbase * np.sin(np.deg2rad(-self.rotation))]
            ), 
            np.array([0.02, 0.03]), 
            self.rotation,
            (255, 0, 0)
        )

        # draw sensors
        X = np.linspace(-self.sensor_width / 2, self.sensor_width / 2, self.sensor_n)
        for num in X:
            p = _rotate_point_around_center(self.position + np.array([num, self.lenght]), self.position, np.deg2rad(-self.rotation))
            graphic_engine.draw_rectangle(
                p, 
                np.array([0.01, 0.01]), 
                self.rotation,
                (64, 64, 255)
            )

 
def _rotate_point_around_center(point, center, angle):
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


if __name__ == "__main__":
    r = Robot(
        max_motor_speed=1.0,
        wheelbase=[0.2, 0.2],
        lenght=[0.14, 0.2],
        engine_cutoff=0.005,
        rotation=0.0,
        sensor_width=[0.1, 0.05],
        sensor_n=8,
        sensor_noise=0.0,
        sensor_radius=0.005,
        min_speed=0.1,
        position=[0.0, 0.0],
        track_width=0.018
    )
    
    t = track.Track()
    for _ in range(4):
        t.add_segment("straight")

    t.finalize(10)
    
    # t.show_track()
    print(r.get_sensors(t))