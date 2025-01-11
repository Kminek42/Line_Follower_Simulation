import pygame
import math
import numpy as np

class GraphicEngine:
    def __init__(self, screen, width, height):
        pygame.init()

        self.screen_res = np.array([width, height])
        self.screen = screen

        self.camera_FOV = 1
        self.camera_pos = np.array([0, 0])


    def clear_screen(self):
        self.screen.fill((255, 255, 255))

    
    def draw_rectangle(self, position, size, rotation, color):
        posX, posY = self.euclid_to_pixels(position.reshape(1, -1))[0]

        sizeX = size[0] * self.screen_res[1] / self.camera_FOV
        sizeY = size[1] * self.screen_res[1] / self.camera_FOV

        rect_center = (posX, posY)
        rect_width, rect_height = sizeX, sizeY
        angle_degrees = rotation

        # Calculate the rotated rectangle
        angle_radians = math.radians(angle_degrees)
        cos_theta = math.cos(angle_radians)
        sin_theta = math.sin(angle_radians)

        points = [
            (-rect_width / 2, -rect_height / 2),
            (rect_width / 2, -rect_height / 2),
            (rect_width / 2, rect_height / 2),
            (-rect_width / 2, rect_height / 2)
        ]

        rotated_points = []
        for point in points:
            x = rect_center[0] + (point[0] * cos_theta - point[1] * sin_theta)
            y = rect_center[1] + (point[0] * sin_theta + point[1] * cos_theta)
            rotated_points.append((x, y))

        # Draw the rotated rectangle on the provided screen
        pygame.draw.polygon(self.screen, color, rotated_points)


    def draw_track(self, track):
        pygame.draw.lines(self.screen, color=(0, 0, 0), closed=False, points=self.euclid_to_pixels(track.chain), width=int(track.line_width * self.screen_res[1] / self.camera_FOV))

    def euclid_to_pixels(self, object_pos):
        # Shift object position relative to the camera
        shifted_pos = object_pos - self.camera_pos
        
        # Scale the coordinates based on zoom factor
        scaled_pos = shifted_pos * self.screen_res[1] / self.camera_FOV
        # Invert Y-axis
        scaled_pos[:, 1] *= -1
        
        # Convert scaled coordinates to pixel coordinates
        pixel_x = (scaled_pos[:, 0] + self.screen_res[0] / 2).astype(np.int32)
        pixel_y = (scaled_pos[:, 1] + self.screen_res[1] / 2).astype(np.int32)
        
        # Return the pixel coordinates as a tuple

        return np.vstack((pixel_x, pixel_y)).T

    def show_content(self):
        pygame.display.flip()