import pygame, os, random
from Tetris import Shape
from Settings import *
pygame.init()
pygame.font.init()
# May 2025

# FIX: grid pos is getting messed up again

# Final Touches: implementing final design
    # show next shape at correct y 
    # shadow cast is visible on every movement 
    # aestetic: game music
    # move shape down fast on down button pressed  


def start_screen():
    title_img = pygame.transform.scale(pygame.image.load(os.path.join(
        "tetris folder", "title img.png")), (WIDTH + 50, HEIGHT - 150))
    title_music = pygame.mixer.Sound(os.path.join("sounds", "8bit 2.wav"))
    title_music.set_volume(0.1)
    title_music.play()

    # start_font = pygame.font.Font(os.path.join("Fonts", "pixel font.ttf"), 15)
    start_text =  FONT.render("Press Space to Start", 1, "white")

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

    screen.blit(screen_bg, (0, 0))
    pygame.draw.rect(screen_bg, (100, 150, 200, 100), [0, 0, WIDTH, HEIGHT])
    screen.blit(pause_text, ((WIDTH / 2 - pause_text.get_width() / 2),
                              HEIGHT / 2 - pause_text.get_height()))
    screen.blit(resume_text, ((WIDTH / 2 - resume_text.get_width() / 2), HEIGHT / 2 + 35))
    pygame.draw.rect(screen, "white", screen_border, 5)

def game_over_screen():
    # game_over_sound.play()
    screen.blit(screen_bg, (0, 0))
    pygame.draw.rect(screen_bg, (50, 50, 50, 200), [0, 0, WIDTH, HEIGHT])
    pygame.draw.rect(screen, "black", screen_border, 7)

    # game over text: press enter to play again or press q to quit 
    game_over_font = pygame.font.Font(os.path.join("Fonts", "pixel font.ttf"), 42)
    game_over_text =  game_over_font.render("Game Over", 1, "blue")
    screen.blit(game_over_text, ((WIDTH / 2 - game_over_text.get_width() / 2),
                            HEIGHT / 2 - game_over_text.get_height() - 20))

    play_again_text = FONT.render("[Press 'Enter' to Play Again]", 1, "white")
    screen.blit(play_again_text, ((WIDTH / 2 - play_again_text.get_width() / 2 + 5),
                                    HEIGHT / 2 + 35))
    
    or_text =  FONT.render("or", 1, "white")
    screen.blit(or_text, ((WIDTH / 2 - or_text.get_width() / 2 + 5),
                            HEIGHT / 2 + 70))
    
    quit_text =  FONT.render("[Press 'Q' to Quit]", 1, "white")
    screen.blit(quit_text, ((WIDTH / 2 - quit_text.get_width() / 2 + 5),
                            HEIGHT / 2 + 105))
        
def check_game_over():
    global game_over, score, lines_done, new_shape, reset

    for block in new_shape.blocks:
        if (block.pos.y <= top_wall and
                    new_shape.vertical_collision(move_dist, new_shape.blocks)):
            game_over = True 

    if reset: # player chooses to play again 
        for row in range(ROWS):
            field_data[row] = [0] * COLUMNS
        new_shape.shadow = []
        all_blocks.empty()
        score = 0
        lines_done = 0
        game_over = False
        new_shape = Shape(all_blocks, "Z_shape")
        reset = False

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
    global lines_done, score

    # find complete rows
    delete_rows = []
    for i, row in enumerate(field_data):
        if all(row): # if there is block in every space of the row 
            delete_rows.append(i)
            lines_done += 1
            score += 100
    
    if delete_rows:
        # delete_sound.play()
        # remove blocks in completed rows + from field_data 
        for delete_row in delete_rows:
            for block in field_data[delete_row]:
                all_blocks.remove(block)
                block.kill()
            field_data[delete_row] = [0] * COLUMNS
         
            for block in all_blocks.sprites(): # shift blocks down by 1 row 
                if block.grid_pos[1] < delete_row:
                    block.pos.y += 1
                    block.update()
                    
        for row in range(ROWS):  # reset field_data board 
            field_data[row] = [0] * COLUMNS
     
        for block in all_blocks.sprites(): # rebuild field data with new block positions
            field_data[block.grid_pos[1]][block.grid_pos[0]] = block

    return field_data

# game window layout - box areas for grid, lines, score 
def draw_layout():

    #  playing area
    playing_box = pygame.Rect(box_left - b_offset, 100 - b_offset,
                                box_width + b_offset*2, box_height + b_offset*2)
    pygame.draw.rect(screen, border_color, playing_box, b_offset)

    # draw grid, width - 10, height - 20
    for col in range(COLUMNS): 
        for row in range(ROWS):
            grid = pygame.Rect(box_left + (col * block_size), 100 + (row * block_size),
                                block_size - 1, block_size - 1 )
            pygame.draw.rect(screen, grid_color, grid, 1)

    # lines area 
    lines_box = pygame.Rect(playing_box.left, 25, playing_box.width, 60)
    pygame.draw.rect(screen, border_color, lines_box, b_offset) # border

    #  score area
    score_box = pygame.Rect(WIDTH - 150, lines_box.top, 125, 125)
    pygame.draw.rect(screen, border_color, score_box, b_offset) # border

    #  next shape area
    next_shape_box = pygame.Rect(score_box.left, score_box.bottom + 20, 100, 150)
    pygame.draw.rect(screen, border_color, next_shape_box, b_offset) # border

    # next shape 
    next_shape_text = FONT.render("Next", 1, "white")

    n_shape = all_shapes[next_shape]["positions"]
    for pos in n_shape:
        next_width = all_shapes[next_shape]["size"][0] 
        next_height = all_shapes[next_shape]["size"][1]

        next_x = next_shape_box.centerx + (pos[0] * block_size) - (block_size * next_width) / 2
        next_y = next_shape_box.centery + next_shape_text.get_height() + (
                    pos[1] * block_size) - (block_size * next_height) / 2

        next_block = pygame.Rect(next_x, next_y, block_size - 1, block_size - 1)
        pygame.draw.rect(screen, all_shapes[next_shape]["color"] , next_block)

    # Text 
    lines_text = FONT.render("Lines-" + str(lines_done), 1, "white")
    score_text = FONT.render("Score", 1, "white")
    score_num = FONT.render(str(score), 1, "white")

    screen.blit(lines_text, (lines_box.centerx - lines_text.get_width() // 2,
                             lines_box.centery - lines_text.get_height() // 2))
    screen.blit(score_text, (score_box.centerx - score_text.get_width() // 2,
                              score_box.y + (score_text.get_height() // 2) + 20))
    screen.blit(score_num, (score_box.centerx - score_num.get_width() // 2,
                              score_box.centery - (score_num.get_height() // 2) + 10))
    screen.blit(next_shape_text, (next_shape_box.centerx - next_shape_text.get_width() // 2,
                    next_shape_box.y + (next_shape_text.get_height() // 2) + 10))


def game_window():

    all_blocks.update()
    game_bg = pygame.transform.scale(pygame.image.load(os.path.join
                            ("tetris folder", "testbg.jpg")), (WIDTH, HEIGHT))
    screen.blit(game_bg, (0, 0))
    # fill playing_box with black 
    screen.fill("black", pygame.Rect(box_left - b_offset, 100 - b_offset,
                            box_width + b_offset*2, box_height + b_offset*2))

    all_blocks.draw(screen)
    for block in all_blocks:
        block.update() # update block grid positions 

    draw_layout()

    new_shape.make_shadow(all_blocks)
    for square in new_shape.shadow:
        pygame.draw.rect(screen, new_shape.color, square, 2)


    if new_shape.game_pause:
        pause_screen()
    
    if game_over:
        game_over_screen()

    pygame.display.update()

#  MAIN:

# start_screen()

new_shape = Shape(all_blocks, random.choice(list(all_shapes.items()))[0])
next_shape = random.choice(list(all_shapes.items()))[0]
next_shape = "Z_shape"
running = True

# game_music.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                new_shape.move(event, all_blocks)
            else:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_RETURN:
                    reset = True

    shape_gravity()
    check_game_over()

    if new_shape.locked and not game_over:
        score += new_shape.blocks[0].grid_pos[1]
        for shadow in new_shape.shadow:
            all_blocks.remove(shadow)
        # lock_sound.play()
        field_data = check_lines(field_data, all_blocks)
        new_shape = Shape(all_blocks, next_shape)
        next_shape = random.choice(list(all_shapes.items()))[0]

    game_window()

pygame.quit()
