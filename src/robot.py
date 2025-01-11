import numpy as np
import matplotlib.pyplot as plt
import track

class Robot:
    def __init__(
        self, 
        *,
        number_of_robots: int,
        
        max_acceleration: float,
        max_speed: float,
        acceleration_coefficient: float,
        
        wheelbase: float, 
        
        position: list[float, float], 
        rotation: float, 
        sensor_positions: np.array,
        sensor_noise: float,
        sensor_radius: float,
        track_width: float
    ):
        assert isinstance(number_of_robots, int) and number_of_robots > 0, "number_of_robots must be positive integer."
        
        assert isinstance(max_acceleration, float) and max_acceleration > 0, "max_acceleration must be positive number."
        assert isinstance(max_speed, float) and max_speed > 0, "max_speed must be positive number."
        assert isinstance(acceleration_coefficient, float) and acceleration_coefficient > 0, "acceleration_coefficient must be positive number."
        
        assert isinstance(wheelbase, float) and wheelbase > 0, "wheelbase must be positive number."
        
        assert isinstance(position, list) and len(position) == 2, "position must be list with X and Y coordinate."
        assert isinstance(rotation, float) and 0 <= rotation <= 2*np.pi, "rotation must be number in range [0, 2*pi]."
        
        assert isinstance(sensor_positions, np.ndarray) and sensor_positions.shape[1] == 2, "sensor_positions must be list of X and Y coordinates."
        assert isinstance(sensor_noise, float) and 0 <= sensor_noise <= 1, "sensor_noise must be number in range [0, 2*pi]."
        assert isinstance(sensor_radius, float) and sensor_radius > 0, "sensor_radius must be positive number."
        assert isinstance(track_width, float) and track_width > 0, "track_width must be positive number."

        self.number_of_robots = number_of_robots
        
        self.max_acceleration = max_acceleration
        self.max_speed = max_speed
        self.acceleration_coefficient = acceleration_coefficient
        
        self.wheelbase = wheelbase
        
        self.position = np.array(position).reshape(1, -1).repeat(number_of_robots, 0)
        self.rotation = np.array([rotation]).repeat(number_of_robots, 0)
        
        self.sensor_positions = sensor_positions
        self.sensor_noise = sensor_noise
        self.sensor_radius = sensor_radius
        self.track_width = track_width
        
        self.motor_speed = np.zeros((self.number_of_robots, 2))

        self.distance_traveled = np.zeros((self.number_of_robots, ))

    def move(self, target_motor_speed, dt):
        assert target_motor_speed.ndim == 2, 'Inputs must be a 2D array (batch_n, 2).'
        assert target_motor_speed.shape[0] == self.number_of_robots, 'Inputs must have same batch size.'
        assert target_motor_speed.shape[1] == 2, 'Inputs must have 2 columns (left and right target_motor_speed).'
        
        non_zero_sign = lambda x: 2 * (x >= 0) - 1
        
        # forward acceleration in limited by acceleration curve, breaking is limited by max acceleration
        target_acceleration = (target_motor_speed * self.max_speed - self.motor_speed) * self.acceleration_coefficient
        acceleration_limit = self.max_acceleration * (1 - self.motor_speed / self.max_speed)
        acceleration = target_acceleration * non_zero_sign(self.motor_speed)
        acceleration = np.maximum(-self.max_acceleration, np.minimum(acceleration, acceleration_limit))
        acceleration = acceleration * non_zero_sign(self.motor_speed)
        # print(f'Acceleration: {acceleration}')
        self.motor_speed += acceleration * dt

        # move robot
        V = self.motor_speed.mean(axis=1)
        w = (self.motor_speed[:, 1] - self.motor_speed[:, 0]) / self.wheelbase
        
        translation = np.array([
            np.cos(self.rotation) * V,
            np.sin(self.rotation) * V
        ]).T

        self.position += translation * dt
        self.rotation += w * dt

        self.distance_traveled += V * dt
        
        return V

    def reset(self):
        self.motor_speed *= 0
        self.position *= 0
        self.rotation = np.radians(90)
        
    def get_sensor_positions(self) -> np.array:
        rot_matrix = np.array([
            [np.cos(self.rotation), -np.sin(self.rotation)],
            [np.sin(self.rotation), np.cos(self.rotation)]
        ])
        positions = np.einsum('mnr, sn -> rsm', rot_matrix, self.sensor_positions)
        sensor_n = len(self.sensor_positions)
        positions += self.position.repeat(sensor_n, axis=0).reshape(-1, sensor_n, 2)
        positions = positions.reshape(-1, 2)
        return positions

    def get_sensors(self, track: track.Track) -> np.array:
        positions = self.get_sensor_positions()
        
        readings = track.distance_to_chain(positions)
        readings = (self.sensor_radius + self.track_width / 2 - readings) / self.sensor_radius
        readings = np.clip(readings, 0.0, 1.0)
        readings += self.sensor_noise * np.random.randn(self.number_of_robots * len(self.sensor_positions))
        readings = np.clip(readings, 0.0, 1.0)
        readings = readings.reshape(self.number_of_robots, len(self.sensor_positions))
        
        return readings
    
    def get_distance(self, track: track.Track):
        '''Returns the distance from robot to the track'''
        return track.distance_to_chain(self.position)
    
    def get_all_positions(self):
        rotation = np.rad2deg(self.rotation[0] - np.pi/2)
        positions = {}
        positions['main body'] = self.position
        positions['wheels'] = [self.position[0][0] - 0.5 * self.wheelbase * np.cos(np.deg2rad(rotation)),
                self.position[0][1] + 0.5 * self.wheelbase * np.sin(np.deg2rad(-rotation))]
        positions['sensors'] = self.get_sensor_positions()
        
        return positions

    def draw(self, graphic_engine):
        rotation = np.rad2deg(self.rotation[0] - np.pi/2)
        # draw breadboard
        graphic_engine.draw_rectangle(
            self.position[0], 
            np.array([0.03, 0.06]), 
            -rotation,
            (32, 255, 32)
        )

        # draw right wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0][0] + 0.5 * self.wheelbase * np.cos(np.deg2rad(rotation)),
                self.position[0][1] - 0.5 * self.wheelbase * np.sin(np.deg2rad(-rotation))]
            ), 
            np.array([0.02, 0.03]), 
            -rotation,
            (255, 32, 32)
        )

        # draw left wheel
        graphic_engine.draw_rectangle(
            np.array([
                self.position[0][0] - 0.5 * self.wheelbase * np.cos(np.deg2rad(rotation)),
                self.position[0][1] + 0.5 * self.wheelbase * np.sin(np.deg2rad(-rotation))]
            ), 
            np.array([0.02, 0.03]), 
            -rotation,
            (255, 32, 32)
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
        number_of_robots=1,
        max_acceleration=1.0,
        max_speed=1.0,
        acceleration_coefficient=1.0,
        wheelbase=0.2,
        position=[0.0, 0.0],
        rotation=0.0,
        sensor_positions=np.array([[-0.01, 0.2], [0.0, 0.2], [0.01, 0.2]]),
        sensor_noise=0.0,
        sensor_radius=0.005,
        track_width=0.018
    )
    
    t = track.Track()
    for _ in range(4):
        t.add_segment("straight")

    t.finalize(10)
    for _ in range(90):
        r.move(np.array([
            [1, 1],
        ]), dt=1e-2)
    for _ in range(90):
        r.move(np.array([
            [-1, -1],
        ]), dt=1e-2)
        
    # print(r.position)
    # print(r.rotation)
    # print(r.get_sensors(t))