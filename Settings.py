import pygame

WIDTH, HEIGHT = 500, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tetris again but this time i actually know stuff")

clock = pygame.time.Clock()
fall_time = 0
rotate_time = 200

block_size = 25
left_wall =  5  # 125 / block_size
right_wall = 15  # 375 / block_size
bottom_wall = 20  # (height - block_size) / block_size

COLUMNS = 10
ROWS = 20

move_dist = 1
block_offset = pygame.Vector2(9, 4)

field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)] # grid for current shapes on screen
locked_shapes = pygame.sprite.Group()