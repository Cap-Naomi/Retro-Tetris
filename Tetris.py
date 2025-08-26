import pygame, random, time
from block_pos import all_blocks
# May 2025

WIDTH, HEIGHT = 500, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tetris again but this time i actually know stuff")

clock = pygame.time.Clock()
fall_time = 0

block_size = 25
left_wall = 125
right_wall = 375


"""   
TO-DO:
- collisions with other blocks 
- rotations
"""

def draw_grid(): # width 10, height 20 
    for col in range(10): 
        for row in range(20):
            grid = pygame.Rect(125 + (col * block_size), 25 + (row * block_size), block_size - 1, block_size - 1)
            pygame.draw.rect(screen, "gray", grid, 1)


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = 200, 25  
        self.rotation = 0 # starts at first position
        self.shape = random.choice(list(all_blocks.items()))[0] # getting random shape from dictionary
        # self.shape = "J_block"
        self.color = all_blocks[self.shape]["color"]
        self.blocks = [] # the full shape made of blocks
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)
        self.locked = False
        
    def get_shape(self): # creating shape object from multiple rects
        block_pos = all_blocks[self.shape]["positions"][self.rotation]
        for col in range(len(block_pos)):
            for row in range(len(block_pos[col])):
                    if block_pos[col][row] == "1":
                        block = pygame.Rect(self.x + (block_size * row), self.y + (block_size * col), block_size - 1, block_size - 1)
                        self.blocks.append(block)

    # check if current block x pos + block_size will put shape out of bounds
    def horizontal_collision(self, amount): 
        for block in self.blocks:
            new_x = block.x + amount
            if new_x not in range(left_wall, right_wall):
                return True

    # allow x movement if horizontal_collision is false
    def move_horizontal(self, amount):
        if not self.horizontal_collision(amount):
            for block in self.blocks:
                block.x += amount

    def vertical_collision(self, amount):
        for block in self.blocks:
            new_y = block.y + amount
            if new_y > HEIGHT - (block_size * 2):
                return True


    # making shape fall at certain speed
    def falling_motion(self):
        global fall_time
        fall_speed = 0.4
        fall_time += clock.get_rawtime() # gets the last time since clock.tick() called
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0 # reset fall time
            if not self.vertical_collision(block_size):
                for blocks in self.blocks: # move each block of shape
                    blocks.y += block_size
            else:
                locked_shapes.add(self)
                self.locked = True


    def move(self):
        if event.key == pygame.K_RIGHT:
            self.move_horizontal(block_size)
        if event.key == pygame.K_LEFT:
            self.move_horizontal(-block_size)       

        if event.key == pygame.K_DOWN:
            if not self.vertical_collision(block_size):
                for blocks in self.blocks: # move each block of shape
                    blocks.y += block_size
            
            
    def rotate(self): # what position do i want to start the next shape at basically
        if event.key == pygame.K_UP:
            # get certain column and row - block farthest to the left and top

            self.blocks.clear() # delete current shape at rotation

            if self.rotation < len(all_blocks[self.shape]["positions"]) - 1:
                self.rotation += 1
            else:
                self.rotation = 0

            self.get_shape() # creates new rotated shape


        # take middle most block and set the self.x and y there
        


locked_shapes = pygame.sprite.Group()


new_shape = Shape()
new_shape.get_shape()
# all_shapes.add(new_shape)

def game_window():
    screen.fill("navy blue")

    # for shape in all_shapes:
    for block in new_shape.blocks:
        pygame.draw.rect(screen, new_shape.color, block)
    
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
        new_shape.get_shape()

    game_window()


pygame.quit()