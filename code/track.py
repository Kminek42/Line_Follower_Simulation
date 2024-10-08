import numpy as np
from matplotlib.pyplot import axis, plot, show
import timeit
import time
from scipy.spatial import KDTree
import math

class Track:
    def __init__(self, line_width = 0.018, tile_size = 0.25):
        self.chain = np.array([0, 0])
        self.line_width = line_width
        self.angle = 0
        self.tile_size = tile_size

        self.segments = {
            "90_right": np.array([[0, 0], [0, 1.0], [1.0, 1.0]]),
            "smooth_right": np.array([[0.0, 0.0], [0.08, 0.38], [0.29, 0.71], [0.62, 0.92], [1.0, 1.0]]),
            "straight": np.array([[0, 0], [0, 1]]),
            "x-intersection": np.array([[0, 0], [0, 0.5], [1, 0.5], [-1, 0.5], [0, 0.5], [0, 1]]),
            "90_left": np.array([[0, 0], [0, 1.0], [-1.0, 1.0]]),
            "smooth_left": np.array([[0.0, 0.0], [-0.08, 0.38], [-0.29, 0.71], [-0.62, 0.92], [-1.0, 1.0]]),
        }
        
    def add_segment(self, segment_type):
        if not segment_type in self.segments:
            if self.angle < -80:
                segment_type = np.random.choice(list(self.segments.keys())[:-2])

            elif self.angle < 80:
                segment_type = np.random.choice(list(self.segments.keys())[:])

            else:
                segment_type = np.random.choice(list(self.segments.keys())[2:])

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

    def finalize(self, subdivisions):
        t = self.chain
        num_segments = len(t) - 1
        interpolated_points = []
        for i in range(num_segments):
            segment_points = np.linspace(t[i], t[i + 1], num=subdivisions)
            interpolated_points.append(segment_points)
        interpolated_points = np.concatenate(interpolated_points)

        self.quadtree = KDTree(interpolated_points)
    
    def distance_to_chain(self, P):
        '''Calculates distance between points P (:, 2) and interpolated track'''
        if P.ndim == 1:
            P = P[np.newaxis, :]

        # Query quadtree to find closest points
        distances, _ = self.quadtree.query(P, k=1)

        return distances
    
    def show_track(self):
        plot(self.chain[:, 0], self.chain[:, 1])
        axis("equal")
        show()
        

if __name__ == "__main__":
    t = Track()
    for _ in range(80):
        t.add_segment("")
    print(t.chain.shape)
    t.finalize(128)
    points = np.array([[0.1, 0.51], [-0.4, 0.0], [0.01, 0.1], [-0.02, 0.2137]])

    a = t.distance_to_chain(points)
    print(a)

    t.show_track()