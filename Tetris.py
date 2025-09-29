import pygame, random, time
from block_pos import all_blocks
# May 2025

WIDTH, HEIGHT = 500, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tetris again but this time i actually know stuff")

clock = pygame.time.Clock()
fall_time = 0

block_size = 25
left_wall =  5  # 125 / block_size
right_wall = 15  # 375 / block_size
bottom_wall = 22  # (height - block_size) / block_size

COLUMNS = 10
ROWS = 20

move_dist = 1

"""   
TO-DO:
- collisions with other blocks 
- rotations
"""
block_offset = pygame.Vector2(9, 4)


class Block(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        super().__init__()

        self.pos = pygame.Vector2(pos) + block_offset
        self.rect = pygame.Rect(self.pos.x * block_size, self.pos.y * block_size, block_size - 1, block_size - 1)
    
    def update(self):
        self.rect.topleft = self.pos * block_size


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.x, self.y = 200, 25  
        self.shape = random.choice(list(all_blocks.items()))[0] # getting random shape from dictionary
        self.color = all_blocks[self.shape]["color"]
        self.rotation = 0 # starts at first position

        self.block_pos = all_blocks[self.shape]["positions"]
        self.blocks = [Block(self.color, pos) for pos in self.block_pos] # the full shape made of blocks
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)

        self.locked = False

        self.field_data = field_data

    # allow x movement if horizontal_collision is false
    def move_horizontal(self, amount):
        if not self.horizontal_collision(amount):
            for block in self.blocks:
                block.pos.x += amount

    # check if current block x pos + block_size will put shape out of bounds
    def horizontal_collision(self, amount): 
        for block in self.blocks:
            new_x = block.pos.x + amount
            if new_x not in range(left_wall, right_wall):
                return True
            
           # if field_data[new_x][block.pos.y] == True: # if there is a block in the space you wanna move to
           #     return True

    def vertical_collision(self, amount):
        for block in self.blocks:
            new_y = block.pos.y + amount 
            if new_y > bottom_wall - (amount * 2):
                return True


    # making shape fall at certain speed
    def falling_motion(self):
        global fall_time
        fall_speed = 0.4
        fall_time += clock.get_rawtime() # gets the last time since clock.tick() called
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0 # reset fall time
            if not self.vertical_collision(move_dist):
                for blocks in self.blocks: # move each block of shape
                    blocks.pos.y += move_dist
            else:
                for block in self.blocks: #+++ need to get block col/row in relation to grid not whole screen 
                    print(f"blocky: {bottom_wall - block.pos.y}, blockx: {block.pos.x}")
                    self.field_data[19][9] = 1 # storing blocks in field_data
                    pass
                # print(self.field_data)
                locked_shapes.add(self)
                self.locked = True

    def move(self):
        if event.key == pygame.K_RIGHT:
            self.move_horizontal(move_dist)
        if event.key == pygame.K_LEFT:
            self.move_horizontal(-move_dist)       

        if event.key == pygame.K_DOWN:
            if not self.vertical_collision(move_dist):
                for blocks in self.blocks: # move each block of shape
                    blocks.pos.y += move_dist
            
            
    def rotate(self):
        pass
        
field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)] # grid for current shapes on screen

locked_shapes = pygame.sprite.Group()

new_shape = Shape()

def draw_grid(): # width 10, height 20 
    for col in range(COLUMNS): 
        for row in range(ROWS):
            grid = pygame.Rect(125 + (col * block_size), 25 + (row * block_size), block_size - 1, block_size - 1)
            pygame.draw.rect(screen, "gray", grid, 1)
            

def game_window():
    screen.fill("navy blue")

    # for shape in all_shapes:
    for block in new_shape.blocks:
        pygame.draw.rect(screen, new_shape.color, block)
        block.update()
    
    for shape in locked_shapes:
        for block in shape.blocks:
            pygame.draw.rect(screen, shape.color, block)
        
    
    draw_grid()
    pygame.display.update()


running = True
while running:
    new_shape.falling_motion()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_shape.move()
            new_shape.rotate()

    if new_shape.locked == True:
        new_shape = Shape()

    game_window()


pygame.quit()
