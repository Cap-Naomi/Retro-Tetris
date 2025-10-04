import pygame, random, time
from block_pos import all_blocks
from Settings import *
# May 2025

class Block(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        super().__init__()

        self.pos = pygame.Vector2(pos) + block_offset
        self.rect = pygame.Rect(self.pos.x * block_size, self.pos.y * block_size, block_size - 1, block_size - 1)
    
    def update(self):
        self.rect.topleft = self.pos * block_size

    def rotate(self, pivot_pos):
        
        distance = self.pos - pivot_pos
        rotated = distance.rotate(90)
        new_pos = pivot_pos + rotated
        return new_pos

class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.shape = random.choice(list(all_blocks.items()))[0] # getting random shape from dictionary
        self.color = all_blocks[self.shape]["color"]
        self.rotation = 0 # starts at first position

        self.block_pos = all_blocks[self.shape]["positions"]
        self.blocks = [Block(self.color, pos) for pos in self.block_pos] # the full shape made of blocks

        self.locked = False

        self.field_data = field_data

    # check if current block x pos + block_size will put shape out of bounds
    def horizontal_collision(self, amount): 
        for block in self.blocks:
            new_x = block.pos.x + amount
            if new_x not in range(left_wall, right_wall):
                return True
            
            # if there is a block in the space it would move to
            if field_data[int(block.pos.y - 1)][int(new_x - left_wall)] == 1:
                return True

    def vertical_collision(self, amount):
        for block in self.blocks:
            new_y = block.pos.y + amount 
            if new_y > bottom_wall:
                return True
            
            # print(f"new y - 1: {new_y - 1}, b.pos.x - left wall: {block.pos.x - left_wall} ")
            if field_data[int(new_y - 1)][int(block.pos.x - left_wall)] == 1: 
                return True
            
    def rotate_collision(self, new_block_pos):
        for pos in new_block_pos:
            if pos.x - left_wall not in range(left_wall, right_wall):
                return False
    
            if pos.y - 1 > bottom_wall:
                return False
        
            if field_data[int(pos.y - 1)][int(pos.x - left_wall)] == 1:
                return False


    # making shape fall at certain speed
    def falling_motion(self):
        global fall_time
        fall_speed = 0.2 #0.4
        fall_time += clock.get_rawtime() # gets the last time since clock.tick() called
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0 # reset fall time
            if not self.vertical_collision(move_dist):
                for blocks in self.blocks: # move each block of shape
                    blocks.pos.y += move_dist
            else:
                for block in self.blocks:
                    field_data[int(block.pos.y - 1)][int(block.pos.x - left_wall)] = 1 # storing blocks in field_data
                
                locked_shapes.add(self)
                self.locked = True

    def move(self, event):
        if event.key == pygame.K_RIGHT:
            if not self.horizontal_collision(move_dist):
                for block in self.blocks:
                    block.pos.x += move_dist

        if event.key == pygame.K_LEFT:
            if not self.horizontal_collision(-move_dist):
                for block in self.blocks:
                    block.pos.x -= move_dist  
        
        if event.key == pygame.K_DOWN:
            if not self.vertical_collision(move_dist):
                for blocks in self.blocks: # move each block of shape
                    blocks.pos.y += move_dist

        if event.key == pygame.K_UP:
            self.rotate(event)
    
    def rotate(self, event):
        if self.shape != "O_block":
            pivot_pos = self.blocks[0].pos # pivot point = position of shape's first block 
            new_block_pos = [block.rotate(pivot_pos) for block in self.blocks]

            if not self.rotate_collision(new_block_pos):
                for j in range(len(self.blocks)):
                    self.blocks[j].pos = new_block_pos[j]

            
            

        
