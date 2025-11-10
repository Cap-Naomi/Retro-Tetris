import pygame, os
from Tetris import Shape
from Settings import *
pygame.init()
pygame.font.init()
# May 2025

# Final Touches: implementing final design
    # keeping track of lines completed 
    # keping track of score - lines * random num probably 
    # show next shape ? - list storing next shape, only add if empty,
        # curr_shape = get and remove list[0], next_shape = list[0]
    # shadow cast is visible on every movement 
    # aestetic: game music, shape colors
    # move shape down fast on down button pressed   
    # end game when hits top line


def start_screen():
    title_img = pygame.transform.scale(pygame.image.load(os.path.join(
        "tetris folder", "title img.png")), (WIDTH + 50, HEIGHT - 150))
    title_music = pygame.mixer.Sound(os.path.join("sounds", "8bit 2.wav"))
    title_music.set_volume(0.1)
    title_music.play()

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
                    title_music.stop()
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

# clear completed rows 
def check_lines(field_data, all_blocks):

    # find complete rows
    delete_rows = []
    for i, row in enumerate(field_data):
        if all(row): # if there is block in every space of the row 
            delete_rows.append(i)
    
    if delete_rows:
        # delete_sound.play()

        # remove blocks in completed rows + from field_data 
        for delete_row in delete_rows:
            for block in field_data[delete_row]:
                all_blocks.remove(block)
                block.kill()
            field_data[delete_row] = [0] * COLUMNS
        
        # shift blocks down by 1 row  
            for block in all_blocks.sprites():
                if block.grid_pos[1] < delete_row:
                    block.pos.y += 1
                    block.update()
                    
        # reset field_data board 
        for row in range(ROWS):
            field_data[row] = [0] * COLUMNS
    
        # rebuild field data with new block positions 
        for block in all_blocks.sprites():
            field_data[block.grid_pos[1]][block.grid_pos[0]] = block

    return field_data



def draw_board2(): 

    # put in grid and make rect for playing window where blocks fall
    # screen.blit(game_bg, (0, -40))
    #   lines made area 
    lines_box = pygame.Rect(73, 25, 214, 75)
    pygame.draw.rect(screen, box_color, lines_box, 0, 10)
    pygame.draw.rect(screen, border_color, lines_box, 7, 10) # border

    #  playing area
    playing_box = pygame.Rect(80, 100 + space, 200, 400)
    playing_box_border = pygame.Rect(playing_box.x - 7, playing_box.y -7, playing_box.width + 14, playing_box.height + 14)
    pygame.draw.rect(screen, box_color, playing_box, 0)
    pygame.draw.rect(screen, border_color, playing_box_border, 7, 10) # border

    num_rows = 20
    num_cols = 10
    box_size = min(playing_box.width // num_cols, playing_box.height // num_rows)
    # --- MAKE GRID FOR TETRIS ---  # 20 rows, 10 cols
    for row in range(num_rows):
        for col in range(num_cols):
            grid = pygame.Rect(playing_box.left + box_size * col, playing_box.top + box_size * row, 20, 20)
            pygame.draw.rect(screen, grid_color, grid, 1)


    #  score / high score area
    score_box = pygame.Rect(320, 25, 225 - space, 150)
    pygame.draw.rect(screen, box_color, score_box, 0, 10)
    pygame.draw.rect(screen, border_color, score_box, 7, 10) # border

    #  next shape area
    next_shape_box = pygame.Rect(320, 200, 225 - space, 200)
    pygame.draw.rect(screen, box_color, next_shape_box, 0, 10)
    pygame.draw.rect(screen, border_color, next_shape_box, 7, 10) # border

    #  quit / pause area
    menu_box = pygame.Rect(320, 400 + space, 225 - space, 107)
    pygame.draw.rect(screen, box_color, menu_box, 0, 10)
    pygame.draw.rect(screen, border_color, menu_box, 7, 10) # border 

    lines_text = FONT.render("Lines", 1, "white")
    score_text = FONT.render("Score", 1, "white")
    next_shape_text = FONT.render("Next Shape", 1, "white")
    menu_text = FONT.render("Menu", 1, "white")


    screen.blit(lines_text, (110, 55))
    screen.blit(score_text, (390, 45))
    screen.blit(next_shape_text, (350, 220))
    screen.blit(menu_text, (395, 435))

# game window layout - box areas for grid, lines, score 
def draw_layout():
    # draw grid, width - 10, height - 20
    for col in range(COLUMNS): 
        for row in range(ROWS):
            grid = pygame.Rect(box_left + (col * block_size), 100 + (row * block_size),
                                block_size - 1, block_size - 1 )
            pygame.draw.rect(screen, "navy", grid, 1)

    #  playing area
    playing_box = pygame.Rect(box_left - b_offset, 100 - b_offset,
                                box_width + b_offset*2, box_height + b_offset*2)
    pygame.draw.rect(screen, border_color, playing_box, 7)

    # lines area 

    # score area 

def game_window():

    all_blocks.update()
    screen.fill("black")
    all_blocks.draw(screen)
    for block in all_blocks:
        block.update() # update block grid positions 

    draw_layout()

    new_shape.make_shadow(all_blocks)
    for square in new_shape.shadow:
        pygame.draw.rect(screen, new_shape.color, square, 2)


    if new_shape.game_pause:
        pause_screen()

    pygame.display.update()

#  MAIN:

# start_screen()

new_shape = Shape(all_blocks)
running = True

# game_music.play()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_shape.move(event, all_blocks)

    # shape_gravity()

    if new_shape.locked == True:
        for shadow in new_shape.shadow:
            all_blocks.remove(shadow)
        # lock_sound.play()
        field_data = check_lines(field_data, all_blocks)
        new_shape = Shape(all_blocks)


    game_window()

pygame.quit()
