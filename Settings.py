import pygame, os
pygame.init()

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
block_offset = pygame.Vector2(9, 2)

field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)] # grid for current shapes on screen
locked_shapes = pygame.sprite.Group()

lock_sound = pygame.mixer.Sound(os.path.join("sounds", "pong mix.wav"))
clear_sound = pygame.mixer.Sound(os.path.join("sounds", "game chime mix.mp3"))

# O, S, I, Z, L, J, T
all_blocks = {
        "O_block" : {
                "positions": [(0, 0), (0,-1), (1, 0), (1, -1)],
                "color": "yellow"
        },

        "S_block" : {
                'positions': [(0, 0), (-1, 0), (0, -1), (1, -1)],
                "color": "green"
        },

        "I_block" : {
                'positions': [(0, 0), (0, -1), (0, -2), (0, 1) ],
                "color": "cyan"
        },

        "Z_block" : {
                'positions': [(0, 0), (1, 0), (0, -1), (1, -1)],
                "color": "red",
        },

        "L_block" : {
                'positions': [(0, 0), (0, -1), (0, 1), (1, 1)],
                "color": "orange"        
        },

        "J_block" : {
                'positions': [(0, 0), (0, -1), (0, 1), (-1, 1)],
                "color": "blue"
        },

        "T_block" : {
            
                'positions': [(0, 0), (-1, 0), (1, 0), (0, -1)],
                "color": "purple"
        },
}
