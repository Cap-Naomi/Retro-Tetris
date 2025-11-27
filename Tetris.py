import pygame, random
from Settings import *
# May 2025

class Block(pygame.sprite.Sprite):
    def __init__(self, group, color, pos):
        super().__init__(group)

        self.pos = pygame.Vector2(pos) + block_offset
        self.rect = pygame.Rect(self.pos.x * block_size, self.pos.y * block_size, 
                                block_size - 1, block_size - 1)
        self.grid_pos = pygame.Vector2(self.pos.x - left_wall, self.pos.y - 1)
        self.image = pygame.Surface((block_size - 1, block_size - 1), pygame.SRCALPHA)
        self.image.fill(color)

    def update(self):
        self.rect.topleft = self.pos * block_size 
        self.grid_pos = (int(self.pos.x - left_wall), int(self.pos.y - 5))

    def rotate(self, pivot_pos):
        distance = self.pos - pivot_pos # distance from pivot to block
        rotated = distance.rotate(90) # rotate distance vector 90 degrees
        new_pos = pivot_pos + rotated 
        return new_pos # new block position after rotation

 # the full shape made of Blocks()
class Shape(pygame.sprite.Sprite):
    def __init__(self, group, curr_shape):
        super().__init__()
        # self.shape = "Z_shape"
        self.shape = curr_shape 
        self.color = all_shapes[self.shape]["color"]

        self.block_pos = all_shapes[self.shape]["positions"]
        self.blocks = [Block(group, self.color, pos) for pos in self.block_pos]
        self.shadow = [Block(group, (0, 0, 0, 0), pos) for pos in self.block_pos]
        self.locked = False
        self.game_pause = False

    def horizontal_collision(self, amount, block_list): 
        for block in block_list:
            new_x = int(block.pos.x + amount)
            if new_x not in range(left_wall, right_wall):
                return True
            
            # if there is a block in the space it would move to
            if field_data[int(block.grid_pos[1])][int(block.grid_pos[0] + amount)]:
                return True

    def vertical_collision(self, amount, block_list):
        for block in block_list:
            new_y = block.pos.y + amount 
            if new_y > bottom_wall:
                return True
            
            if field_data[int(block.grid_pos[1]) + amount][int(block.grid_pos[0])]: 
                return True
            
    def rotate_collision(self, new_block_pos):
        for pos in new_block_pos:

            if pos.x not in range(left_wall, right_wall):
                return True
            
            if pos.y - 1 > bottom_wall:
                return True

            #FIX: this terrible index out of range error
            if field_data[int(pos.y - 5)][int(pos.x - left_wall)]: 
                return True

    def fall_down(self):
        if not self.game_pause and not game_over:
            if not self.vertical_collision(move_dist, self.blocks):
                for blocks in self.blocks: # move each block of shape
                    blocks.pos.y += move_dist
                    
            else:
                for block in self.blocks: # storing blocks in field_data
                    field_data[int(block.grid_pos[1])][int(block.grid_pos[0])] = block 
                self.locked = True

    def make_shadow(self, group): # "shadow effect" showing where block will land 
        check_shadow = [self.vertical_collision(
            move_dist, self.shadow) for block in self.shadow] 
        for i, square in enumerate(self.shadow):   
            if not any(check_shadow):
                square.pos.y += 1       

    def move(self, event, group):
        if not self.game_pause:
            if event.key == pygame.K_RIGHT:
                if not self.horizontal_collision(move_dist, self.blocks):
                    for block in self.blocks:
                        block.pos.x += move_dist

            if event.key == pygame.K_LEFT:
                if not self.horizontal_collision(-move_dist, self.blocks):
                    for block in self.blocks:
                        block.pos.x -= move_dist  
            
            if event.key == pygame.K_DOWN:
                if not self.vertical_collision(move_dist, self.blocks):
                    for block in self.blocks: # move each block of shape
                        block.pos.y += move_dist
                        pass
                        # pygame.time.set_timer(down_timer, 100)
                        #print("hi")
                        # block.pos.y += move_dist

            if event.key == pygame.K_UP: # rotate shape 
                self.rotate(event)

            # recreate shadow on move
            if not event.key == pygame.K_SPACE:
                self.block_pos = [block.pos for block in self.blocks] 
                for shadow in self.shadow:
                    all_blocks.remove(shadow)
                self.shadow = [Block(group, (0, 0, 0, 0),
                            pos - block_offset) for pos in self.block_pos]  

        if event.key == pygame.K_SPACE: # pause the game 
            if not self.game_pause:
                self.game_pause = True
            else:
                self.game_pause = False 
                 
    def rotate(self, event):
        if self.shape != "O_shape":
            pivot_pos = self.blocks[0].pos # pivot point = position of shape's first block 
            new_block_pos = [block.rotate(pivot_pos) for block in self.blocks]

            if not self.rotate_collision(new_block_pos):
                for i, block in enumerate(self.blocks):
                    block.pos = new_block_pos[i]
                
            

        
