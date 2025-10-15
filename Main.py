import pygame, os
from Tetris import Shape
from Settings import *
pygame.init()
pygame.font.init()
# May 2025

# FIX: clear_line and need to make blocks fall down one after
# move shapes down as many lines needed -> then draw on screen 

def start_screen():
    title_img = pygame.transform.scale(pygame.image.load(os.path.join(
        "tetris folder", "title img.png")), (WIDTH + 50, HEIGHT - 150))

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
        screen.blit(title_img, (-25, 25))
        screen.blit(start_text, ((WIDTH / 2) - start_text.get_width() / 2, 390))
        pygame.draw.rect(screen, cyan, screen_border, 5)

        # blinking animation - # if time passed is greater than cooldown
        if pygame.time.get_ticks() - blink_timer >= blink_cooldown: 
            blink_timer = pygame.time.get_ticks()
            pygame.time.set_timer(BLINK_TEXT, 750)
            start_text =  start_font.render("", 0, "white") # make text blank during blink 

        pygame.display.update()

def pause_screen():
    pause_font = pygame.font.Font(os.path.join("Fonts", "pixel font.ttf"), 35)
    pause_text =  pause_font.render("Game Paused", 1, "white")

    resume_font = pygame.font.Font(os.path.join("Fonts", "pixel font.ttf"), 15)
    resume_text =  resume_font.render("[press space to resume]", 1, "white")

    screen.blit(pause_bg, (0, 0))
    pygame.draw.rect(pause_bg, (100, 150, 200, 100), [0, 0, WIDTH, HEIGHT])
    screen.blit(pause_text, ((WIDTH / 2 - pause_text.get_width() / 2),
                              HEIGHT / 2 - pause_text.get_height()))
    screen.blit(resume_text, ((WIDTH / 2 - resume_text.get_width() / 2), HEIGHT / 2 + 35))
    pygame.draw.rect(screen, "white", screen_border, 5)



    

# making shape fall at certain speed
def shape_gravity(): 
    global fall_time
    fall_speed = 0.2 #0.4
    fall_time += clock.get_rawtime() # gets the last time since clock.tick() called
    clock.tick()
    if fall_time / 1000 >= fall_speed:
        fall_time = 0 # reset fall time
        new_shape.fall_down()  

def game_window():

    all_blocks.update()
    screen.fill("black")
    all_blocks.draw(screen)

    # draw grid, width - 10, height - 20
    for col in range(COLUMNS): 
        for row in range(ROWS):
            grid = pygame.Rect(125 + (col * block_size), 25 + (row * block_size),
                                block_size - 1, block_size - 1)
            pygame.draw.rect(screen, "cyan", grid, 1)

    if new_shape.game_pause:
        pause_screen()


    pygame.display.update()

def check_lines():
    delete_rows = []
    for i, row in enumerate(field_data):
        if all(row): # if there is block in every space of the row 
            delete_rows.append(i)
    
    if delete_rows:
        #delete_sound.play()
        for delete_row in delete_rows:
            for block in field_data[delete_row]:
                block.kill()
                field_data[delete_row][block.grid_pos[0]] = 0
            
            for row in field_data:
                for block in row:
                    if block and block.grid_pos[1] < delete_row:
                        block.pos.y += 1

        #field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)] 
        #for block in all_blocks.sprites():
            #field_data[int(block.grid_pos[1])][int(block.grid_pos[0])] = block
                
        #for row in range(ROWS):
            #print(field_data[row])


#  MAIN:
new_shape = Shape(all_blocks)
running = True

#start_screen()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_shape.move(event)

    shape_gravity()

    if new_shape.locked == True:
        #lock_sound.play()
        check_lines()
        new_shape = Shape(all_blocks)

    game_window()

pygame.quit()
