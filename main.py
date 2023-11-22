import pygame
from graphic_engine import GraphicEngine
from track import Track
import numpy as np

pygame.init()

width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Open Polygon')

ge = GraphicEngine(screen, 1024, 768)
ge.camera_FOV = 2
ge.camera_pos = [0, 0.3]
t = Track()
for i in range(10):
    t.add_segment("")

running = True
while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ge.draw_track(t)
    pygame.display.flip()

pygame.quit()

print(t.chain.shape)

print(np.array([[0, 0], [1, 1], [2, 2]]).shape)