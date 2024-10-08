import numpy as np
import matplotlib.pyplot as plt
import track

class Robot:
    def __init__(
        self, 
        *,
        max_motor_speed, 
        wheelbase, 
        engine_acceleration, 
        lenght, 
        position, 
        rotation, 
        sensor_width, 
        sensor_n, 
        sensor_noise,
        min_speed,
        sensor_radius,
        track_width
    ):

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
        assert isinstance(engine_acceleration, float)
        assert isinstance(min_speed, float)
        assert isinstance(sensor_radius, float)
        assert isinstance(track_width, float)

        self.robot_n = wheelbase.shape[0]

        self.position = np.tile(position, (self.robot_n, )).reshape((-1, 2))
        self.rotation = np.array(rotation).repeat(self.robot_n, axis=0)

        self.wheelbase = wheelbase
        self.lenght = lenght

        self.max_motor_speed = max_motor_speed
        self.acceleration = engine_acceleration
        self.min_speed = min_speed

        self.sensor_n = sensor_n
        self.sensor_width = sensor_width
        self.sensor_noise = sensor_noise
        self.sensor_radius = sensor_radius
        self.track_width = track_width

        self.m1_v = 0
        self.m2_v = 0

        self.mileage = np.zeros((self.robot_n, ))


    def move(self, motors, dt):
        assert motors.ndim == 2, 'Inputs must be a 2D array (batch_n, 2).'
        assert motors.shape[0] == self.robot_n, 'Inputs must have same batch size.'
        assert motors.shape[1] == 2, 'Inputs must have 2 columns (left and right motors).'
        
        motor_l, motor_r = motors[:, 0], motors[:, 1]
        
        # limit input
        motor_l = np.clip(motor_l, -1, 1)
        motor_r = np.clip(motor_r, -1, 1)
        
        # apply inertia
        self.m1_v += self.acceleration * np.clip((motor_l - self.m1_v) / dt, -1, 1) * dt
        self.m2_v += self.acceleration * np.clip((motor_r - self.m2_v) / dt, -1, 1) * dt
        
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

        self.mileage += V * dt
        return V

    def get_sensor_positions(self):
        X = np.repeat(self.lenght, self.sensor_n)

        Y = np.linspace(self.sensor_width / 2, -self.sensor_width / 2, self.sensor_n).T.reshape((-1))

        angle = np.repeat(self.rotation, self.sensor_n)

        x_rotated = X * np.cos(angle) - Y * np.sin(angle)
        y_rotated = X * np.sin(angle) + Y * np.cos(angle)

        positions = np.stack((x_rotated, y_rotated), axis=1)
        positions += np.repeat(self.position, self.sensor_n, axis=0)

        return positions

    def get_sensors(self, track: track.Track):
        positions = self.get_sensor_positions()
        
        readings = track.distance_to_chain(positions)
        readings = (self.sensor_radius + self.track_width / 2 - readings) / self.sensor_radius
        readings = np.clip(readings, 0.0, 1.0)
        readings += self.sensor_noise * np.random.randn(self.robot_n * self.sensor_n)
        readings = np.clip(readings, 0.0, 1.0)

        return readings.reshape(self.robot_n, self.sensor_n)
    
    def get_distance(self, track: track.Track):
        '''Returns the distance from robot to the track'''
        return track.distance_to_chain(self.position)

    def draw(self, graphic_engine):
        rotation = np.rad2deg(self.rotation[0] - np.pi/2)
        # draw breadboard
        graphic_engine.draw_rectangle(
            self.position[0], 
            np.array([0.03, 0.06]), 
            -rotation,
            (64, 255, 64)
        )

        # draw right wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0][0] + 0.5 * self.wheelbase * np.cos(np.deg2rad(rotation)),
                self.position[0][1] - 0.5 * self.wheelbase * np.sin(np.deg2rad(-rotation))]
            ), 
            np.array([0.02, 0.03]), 
            -rotation,
            (255, 0, 0)
        )

        # draw left wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0][0] - 0.5 * self.wheelbase[0] * np.cos(np.deg2rad(rotation)),
                self.position[0][1] + 0.5 * self.wheelbase[0] * np.sin(np.deg2rad(-rotation))]
            ), 
            np.array([0.02, 0.03]), 
            -rotation,
            (255, 0, 0)
        )

        # draw sensors
        pos = self.get_sensor_positions()
        for p in pos:
            graphic_engine.draw_rectangle(
                p, 
                np.array([0.005, 0.005]), 
                # np.rad2deg(rotation),
                -rotation,
                (64, 64, 255)
            )


if __name__ == "__main__":
    r = Robot(
        max_motor_speed=1.0,
        wheelbase=[0.2, 0.2],
        lenght=[0.14, 0.2],
        engine_acceleration=0.1,
        rotation=np.pi/2,
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
    for _ in range(90):
        r.move([0.0, 0.0], [0.3, 0.0], 1/100)
    # t.show_track()
        
    print(r.position)
    print(r.rotation)
    print(r.get_sensors(t))