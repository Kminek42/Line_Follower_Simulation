import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree

from enum import Enum

class SegmentType(Enum):
    """Enumeration for segment types."""
    STRAIGHT = "straight"
    RIGHT_90 = "90_right"
    SMOOTH_RIGHT = "smooth_right"
    LEFT_90 = "90_left"
    SMOOTH_LEFT = "smooth_left"
    X_INTERSECTION = "x-intersection"

class Segment:
    def __init__(self, segment_type: SegmentType, points: np.ndarray):
        self.segment_type = segment_type
        self.points = points

class Track:
    def __init__(self, line_width=0.018, tile_size=0.25):
        self.chain = np.array([[0, 0]])
        self.line_width = line_width
        self.angle = 0
        self.tile_size = tile_size

        self.segments = {
            SegmentType.RIGHT_90: Segment(SegmentType.RIGHT_90, np.array([[0, 0], [0, 1.0], [1.0, 1.0]])),
            SegmentType.SMOOTH_RIGHT: Segment(SegmentType.SMOOTH_RIGHT, np.array([[0.0, 0.0], [0.08, 0.38], [0.29, 0.71], [0.62, 0.92], [1.0, 1.0]])),
            SegmentType.STRAIGHT: Segment(SegmentType.STRAIGHT, np.array([[0, 0], [0, 1]])),
            SegmentType.X_INTERSECTION: Segment(SegmentType.X_INTERSECTION, np.array([[0, 0], [0, 0.5], [1, 0.5], [-1, 0.5], [0, 0.5], [0, 1]])),
            SegmentType.LEFT_90: Segment(SegmentType.LEFT_90, np.array([[0, 0], [0, 1.0], [-1.0, 1.0]])),
            SegmentType.SMOOTH_LEFT: Segment(SegmentType.SMOOTH_LEFT, np.array([[0.0, 0.0], [-0.08, 0.38], [-0.29, 0.71], [-0.62, 0.92], [-1.0, 1.0]])),
        }

    def add_segment(self, segment_type: SegmentType = None):
        if segment_type not in self.segments:
            if self.angle < -80:
                segment_type = np.random.choice(list(self.segments.keys())[:-2])

            elif self.angle < 80:
                segment_type = np.random.choice(list(self.segments.keys()))

            else:
                segment_type = np.random.choice(list(self.segments.keys())[2:])

        segment_obj = self.segments[segment_type]

        segment_points = segment_obj.points * self.tile_size

        self.angle = np.radians(self.angle)
        rotation_matrix = np.array([
            [np.cos(self.angle), -np.sin(self.angle)],
            [np.sin(self.angle), np.cos(self.angle)]
        ])
        segment_points = np.dot(segment_points, rotation_matrix)

        segment_points += self.chain[-1]

        self.chain = np.vstack((self.chain, segment_points[1:]))

        self.angle = np.degrees(self.angle)
        if segment_type in {SegmentType.SMOOTH_LEFT, SegmentType.LEFT_90}:
            self.angle -= 90
        elif segment_type in {SegmentType.SMOOTH_RIGHT, SegmentType.RIGHT_90}:
            self.angle += 90
            

    def finalize(self, subdivisions: int = 128):
        t = self.chain
        num_segments = len(t) - 1
        interpolated_points = []
        for i in range(num_segments):
            segment_points = np.linspace(t[i], t[i + 1], num=subdivisions)
            interpolated_points.append(segment_points)
        interpolated_points = np.concatenate(interpolated_points)

        self.quadtree = KDTree(interpolated_points)
    
    def distance_to_chain(self, P: np.array) -> np.array:
        '''Calculates distance between points P (:, 2) and interpolated track'''
        if P.ndim == 1:
            P = P[np.newaxis, :]

        distances, _ = self.quadtree.query(P, k=1)

        return distances
    
    def show_track(self):
        plt.figure(figsize=(4, 4), dpi=200)
        plt.plot(self.chain[:, 0], self.chain[:, 1], '-', color='grey', linewidth=1)
        plt.plot(self.chain[:, 0], self.chain[:, 1], 'o', color='red', markersize=4)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axis("equal")
        plt.show()
        

if __name__ == "__main__":
    np.random.seed(42)
    t = Track()
    t.add_segment(SegmentType.STRAIGHT)
    t.add_segment(SegmentType.SMOOTH_LEFT)
    t.add_segment(SegmentType.X_INTERSECTION)
    t.add_segment(SegmentType.RIGHT_90)
    
    for _ in range(4):
        t.add_segment()
    
    print(t.chain.shape)
    t.finalize(128)
    points = np.array([[0.1, 0.51], [-0.4, 0.0], [0.01, 0.1], [-0.02, 0.2137]])

    a = t.distance_to_chain(points)
    print(a)

    t.show_track()