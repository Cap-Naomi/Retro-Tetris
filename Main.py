import pygame, os
from Tetris import Shape
from Settings import *
pygame.init()
pygame.font.init()
# May 2025

# FIX: clear_line - does not clear lines properly - and need to make blocks fall down one after

def start_screen():
    background = pygame.transform.scale(pygame.image.load(os.path.join("tetris folder", "title img.png")), (WIDTH + 50, HEIGHT - 150))
    border = pygame.Rect(0, 0, WIDTH , HEIGHT)

    start_font = pygame.font.Font(os.path.join("Fonts", "pixel font.ttf"), 15)
    start_text =  start_font.render("Press Space to Start", 1, "white")

    BLINK_TEXT = pygame.USEREVENT + 1
    blink_cooldown = 2000

    blink_timer = pygame.time.get_ticks()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == BLINK_TEXT:
                start_text =  start_font.render("Press Space to Start", 1, "white")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

        screen.fill("black")
        screen.blit(background, (-25, 25))
        screen.blit(start_text, ((WIDTH / 2) - start_text.get_width() / 2, 390))
        pygame.draw.rect(screen, "cyan", border, 5)

        # blinking animation 
        if pygame.time.get_ticks() - blink_timer >= blink_cooldown: # if time passed is greater than cooldown
            blink_timer = pygame.time.get_ticks()
            pygame.time.set_timer(BLINK_TEXT, 750)
            start_text =  start_font.render("", 0, "white") # make text blank during blink 


        pygame.display.update()


def draw_grid(): # width 10, height 20 
    for col in range(COLUMNS): 
        for row in range(ROWS):
            grid = pygame.Rect(125 + (col * block_size), 25 + (row * block_size), block_size - 1, block_size - 1)
            pygame.draw.rect(screen, "cyan", grid, 1)
            

def game_window(new_shape):
    screen.fill("navy blue")

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
    clear_sound.play()
    if delete_row != -1:
        # TO DO: how to remove all blocks from this row, and move blocks above it down 
        for shape in locked_shapes:
            for block in shape.blocks:
                if (block.pos.y - 1) == (bottom_wall - delete_row):
                    print("destroy block")
                    shape.blocks.remove(block)
        
        for col in range(COLUMNS):
            field_data[bottom_wall - delete_row][col] = 0
        
        for row in range(ROWS):
            print(field_data[row])

def check_lines():

    for rows in range(ROWS):
        row_sum = 0
        delete_row = -1
        for val in field_data[rows]:
            row_sum += int(val)
            if row_sum == 10:
                delete_row = val
                clear_line(delete_row)


#  MAIN:
new_shape = Shape()
running = True

start_screen()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_shape.move(event)

    new_shape.falling_motion()

    if new_shape.locked == True:
        lock_sound.play()
        check_lines()
        new_shape = Shape()

    game_window(new_shape)

pygame.quit()

