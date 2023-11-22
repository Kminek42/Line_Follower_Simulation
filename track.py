import numpy as np
import math

class Track:
    def __init__(self, line_width = 0.018, tile_size = 0.25):
        self.chain = np.array([0, 0])
        self.line_width = line_width
        self.angle = 0
        self.tile_size = tile_size

        self.segments = {
            "straight": np.array([[0, 0], [0, 1]]),
            "x-intersection": np.array([[0, 0], [0, 0.5], [1, 0.5], [-1, 0.5], [0, 0.5], [0, 1]]),
            "90_right": np.array([[0, 0], [0, 0.5], [0.5, 0.5]]),
            "90_left": np.array([[0, 0], [0, 0.5], [-0.5, 0.5]]),
            "smooth_right": np.array([[0.0, 0.0], [0.08, 0.38], [0.29, 0.71], [0.62, 0.92], [1.0, 1.0]]),
            "smooth_left": np.array([[0.0, 0.0], [-0.08, 0.38], [-0.29, 0.71], [-0.62, 0.92], [-1.0, 1.0]]),
        }
        
    def add_segment(self, segment_type):
        if not segment_type in self.segments:
            segment_type = np.random.choice(list(self.segments.keys()))

        segment = self.segments[segment_type] * self.tile_size

        self.angle = np.radians(self.angle)
        rotation_matrix = np.array([
            [np.cos(self.angle), -np.sin(self.angle)],
            [np.sin(self.angle), np.cos(self.angle)]
        ])
        
        segment = np.dot(segment, rotation_matrix)
        segment += self.chain[-1]
        
        self.angle = np.degrees(self.angle)
        if segment_type in ["smooth_left", "90_left"]:
            self.angle -= 90

        elif segment_type in ["smooth_right", "90_right"]:
            self.angle += 90

        self.chain = np.vstack((self.chain, segment[1:]))
        
    def distance_to_chain(self, xp, yp):
        '''Calculates distance between point [xp, yp] and chain (array of points)'''

        min_distance = float('inf')

        for i in range(len(self.chain) - 1):
            x1, y1 = self.chain[i]
            x2, y2 = self.chain[i + 1]

            # Calculate the squared distance between the point and the line segment
            dx = x2 - x1
            dy = y2 - y1

            if dx == 0 and dy == 0:
                # If the segment is just a point, calculate the distance to that point
                segment_distance = math.sqrt((xp - x1)**2 + (yp - y1)**2)
            else:
                t = ((xp - x1) * dx + (yp - y1) * dy) / (dx**2 + dy**2)

                if t < 0:
                    segment_distance = math.sqrt((xp - x1)**2 + (yp - y1)**2)
                elif t > 1:
                    segment_distance = math.sqrt((xp - x2)**2 + (yp - y2)**2)
                else:
                    segment_x = x1 + t * dx
                    segment_y = y1 + t * dy
                    segment_distance = math.sqrt((xp - segment_x)**2 + (yp - segment_y)**2)

            # Update the minimum distance
            if segment_distance < min_distance:
                min_distance = segment_distance

        return min_distance
