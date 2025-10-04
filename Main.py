import pygame
from Tetris import Block, Shape
from Settings import *
# May 2025



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

def clear_line(delete_row):
    print(delete_row)
    if delete_row != -1:
        # TO DO: how to remove all blocks from this row, and move blocks above it down 
        for shape in locked_shapes:
            for block in shape.blocks:
                if (block.pos.y - 1) == (bottom_wall - delete_row):
                    print("destroy block")
                    shape.blocks.remove(block)
        
        for col in range(COLUMNS):
            field_data[bottom_wall - delete_row][col] = 2
        
        print(field_data)
                


def check_lines():

    for rows in range(ROWS):
        row_sum = 0
        delete_row = -1
        for val in field_data[rows]:
            row_sum += int(val)
            if row_sum == 10:
                delete_row = val
                clear_line(delete_row)

        

new_shape = Shape()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_shape.move(event)

    new_shape.falling_motion()

    if new_shape.locked == True:
        check_lines()
        new_shape = Shape()

    game_window()

pygame.quit()