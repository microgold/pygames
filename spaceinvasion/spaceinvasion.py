import random
import pygame

from ImageSprite import ImageSprite
from PlayerSprite import PlayerSprite
from BulletSprite import BulletSprite
from InvaderSprite import InvaderSprite
from BombSprite import BombSprite
from HiScoreSprite import HiScoreSprite
from ScoreSprite import ScoreSprite
from MessageSprite import MessageSprite
from LivesSprite import LivesSprite
from SaucerSprite import SaucerSprite

# Set up Pygame
pygame.init()

window_width = 800
window_height = 660

# Set up window
WINDOW_SIZE = (window_width, window_height)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Space Invaders')


# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# create an array of colors
colors = [GREEN, RED, BLUE]

# Set up font
font = pygame.font.Font(None, 36)

# size of piece on board
piece_size = 20

small_font = pygame.font.Font(None, 16)

alien_names = ['invader1', 'invader2', 'invader2', 'invader3', 'invader3' ]

game_time = 0

board_cleared = False

## dictionary for scoring points
score_dict =  {
    'invader1': 30,
    'invader2': 20,
    'invader3': 10
}

def create_aliens():
    global alien_groups, level
    alien_groups = []
    for i in range(0, 5):
        alien_group = pygame.sprite.Group()
        for j in range(0, 11):
            alien = InvaderSprite(alien_names[i], alien_names[i] + 'c', 30 + (j * 60), 100 + i*60, alien_group, score_dict[alien_names[i]], level)
            alien_group.add(alien)
        alien_groups.append(alien_group)

# Set up player logic
player_lives = 3

# set up sounds
alien_dying = pygame.mixer.Sound('sounds/3.wav')
bullet_fire_sound = pygame.mixer.Sound('sounds/1.wav')
player_hit_sound = pygame.mixer.Sound('sounds/2.wav')
alien_movement = pygame.mixer.Sound('sounds/6.wav')
alien_movement2 = pygame.mixer.Sound('sounds/7.wav')
player_dying = pygame.mixer.Sound('sounds/5.wav')
saucer_sound = pygame.mixer.Sound('sounds/8.wav')
saucer_dying = pygame.mixer.Sound('sounds/3.wav')

# set up game sprites
player = PlayerSprite('man', 30, 600)
bullet = BulletSprite(0, 0, 3, 15, .1)
saucer = SaucerSprite('saucer0', 'saucer1', 'saucer2', window_width - 50, 50, 1)
# center game over message
game_over_message = MessageSprite('Game Over', window_width/2 - 80, window_height/2)
play_again_message = MessageSprite('Play again? (y/n)', window_width/2 - 100, window_height/2 + 60)



score_group = pygame.sprite.Group()

hi_score = HiScoreSprite()
score = ScoreSprite()
lives_indicator = LivesSprite(window_width=window_width)


score_group.add(score, hi_score)

def process_events():
    global player_left, player_right, bullet_active, level
    (player_x, player_y) = player.position
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check if player has moved
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                if bullet_active == False and not player.dead:
                    bullet_active = True
                    bullet.position = (player_x + 30, player_y - 20)
                    bullet_fire_sound.play()
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_left = True
                player_right = False
            elif event.key == pygame.K_RIGHT and player_x < window_width:
                player_right = True
                player_left = False
            elif event.key == pygame.K_y and game_over == True:
                initialize_game_state()
            elif event.key == pygame.K_n and game_over == True:
                running = False
        elif event.type == pygame.KEYUP:
            player_left = False
            player_right = False
    return running

def start_saucer():
    if saucer.active == False:
        saucer.reset(window_width - 50, 50, level)
        saucer.active = True
        saucer_sound.play()
        saucer.position = (window_width - 50, 50)

def find_leftmost_alien():
    minimum_x = window_width
    leftmost_alien = None
    for alien_group in alien_groups:
        alien = alien_group.sprites()[0]
        if (alien.position[0] < minimum_x):
            minimum_x = alien.position[0]
            leftmost_alien = alien

    return leftmost_alien

def find_rightmost_alien():
    maximum_x = 0
    rightmost_alien = None
    for alien_group in alien_groups:
        alien = alien_group.sprites()[-1]
        if (alien.position[0] > maximum_x):
            maximum_x = alien.position[0]
            rightmost_alien = alien

    return rightmost_alien

def find_bottommost_alien():
    maximum_y = 999
    bottommost_alien = None
    for alien_group in alien_groups:
        alien = alien_group.sprites()[-1]
        if (alien.position[1] < maximum_y):
            maximum_y = alien.position[0]
            bottommost_alien = alien
    return bottommost_alien


def move_aliens(leftmost, rightmost, bottommost, move_right, move_down):
    global game_time

    last_alien = rightmost
    first_alien = leftmost

    if (last_alien is None) or (first_alien is None):
        return (move_right, move_down)

    (last_alien_x, last_alien_y) = last_alien.position
    (first_alien_x, first_alien_y) = first_alien.position

    # move right and possibly down
    if move_right:
        if last_alien_x + last_alien.speed >= window_width - (last_alien.rect.width + 5):
            move_right = False  
            if last_alien_y + last_alien.speed < window_height - last_alien.rect.height:                
                if (bottommost.position[1] < window_height - 50):
                    move_down = True  
        return move_right, move_down
    
    # move left and possibly down
    if not move_right:
        if first_alien_x - first_alien.speed <= 0:
            move_right = True
            if first_alien_y + first_alien.speed < window_height - first_alien.rect.height:
              if (bottommost.position[1] < window_height - 50):
                    move_down = True  

 

    return move_right, move_down



def check_for_removal(alien):    
        if alien.death_time > 0 and alien.death_time + 250 < pygame.time.get_ticks():
          alien.parent.remove(alien)
          if (len(alien.parent) == 0):
              alien_groups.remove(alien.parent)

def handle_bullet(bullet, bullet_active):
    (bullet_x, bullet_y) = bullet.position
    bullet_y = bullet_y - bullet.speed
    bullet.position = (bullet_x, bullet_y)
    bullet.update()
    bullet.draw(window)
    if (handle_alien_hit(bullet_x, bullet_y)):
        bullet_active = False
        bullet.position = (0, 0)

    if (handle_saucer_hit(bullet_x, bullet_y)):
        bullet_active = False
        bullet.position = (0, 0)

    if (bullet_y < 0):
        bullet_active = False
    
    return bullet_active

def aliens_exist():
    for alien_group in alien_groups:
        if len(alien_group) > 0:
            return True
    return False

def handle_saucer_movement():
    global game_time
    saucer_show_score_time = 1000    

    if saucer.active:
        saucer.move_left()
        saucer.update()
        saucer.draw(window)
        saucer.switch_image(int(game_time/saucer_blink_speed) % 3 )
        (saucer_x, saucer_y) = saucer.position
        if (saucer_x <= -100):
            saucer.dead = True
            saucer.position = (0, 0)

    if saucer.dead:
        current_saucer_death_time = pygame.time.get_ticks() - saucer.death_time 
        if current_saucer_death_time > saucer_show_score_time:
            saucer.active = False


def handle_alien_movement(): 
    global game_time, move_aliens_down, alien_groups, move_aliens_right
    alien_rightmost = find_rightmost_alien()
    alien_leftmost = find_leftmost_alien()
    alien_bottommost = find_bottommost_alien()
    (move_aliens_right, move_aliens_down) = move_aliens(alien_leftmost, alien_rightmost, 
                                                         alien_bottommost, move_aliens_right, move_aliens_down)    

    # do animation
    for alien_group in alien_groups:
        for next_alien in alien_group:
            next_alien.switch_image(int(game_time/blink_speed) % 2 )
            next_alien.update()

    if game_time % 400 == 0 and aliens_exist():
        if game_time % 800 == 0:
            alien_movement.play()    
        else:
            alien_movement2.play()

    for alien_group in alien_groups:
        for alien in alien_group:
            (x,y) = alien.position
            if move_aliens_right:
                alien.move_right()
            else:
                alien.move_left()
            if move_aliens_down:
                alien.move_down()
            alien.update()

    move_aliens_down = False

def handle_saucer_hit(bullet_x, bullet_y):
    global player_score, bullet, saucer
    (x, y) = saucer.position
    if bullet_x > x and bullet_x < x + saucer.get_width() and  \
            bullet_y > y and bullet_y < y + saucer.get_height():
        saucer.kill()                
        saucer_dying.play()
        player_score += saucer.points
        return True
    return False

def handle_alien_hit(bullet_x, bullet_y):
    global gems_collected, player_score, bullet, alien_groups
    for alien_group in alien_groups:
        for alien in alien_group:
            (x, y) = alien.position
            if bullet_x > x and bullet_x < x + alien.get_width() and  \
                 bullet_y > y and bullet_y < y + alien.get_height():
                alien.kill()                
                alien_dying.play()
                player_score += alien.points
                return True
    return False
    
def handle_player_hit(bomb_x, bomb_y):
    global gems_collected, player_score, bullet, alien_groups, player_lives, lives_indicator
    (x, y) = player.position
    if bomb_x > x and bomb_x < x + player.get_width() and \
        bomb_y > y and bomb_y < y + player.get_height() \
        and player.dead == False:
        player.kill()
        player.death_time = pygame.time.get_ticks()
        player_hit_sound.play()
        player_lives = player_lives - 1
        lives_indicator.update_lives(player_lives)
        if (player_lives == 0):
            handle_game_over()
        return True
    return False

def handle_game_over():
    global game_over
    game_over = True


active_bombs = []
bomb_frequency = 5

def check_for_bomb_activation():
     global game_time, active_bombs, alien_groups, bomb_frequency
     if (game_time/1000 % 2 == 0):
        if len(alien_groups) <= 0: return
        # find all aliens that currently have ability to bomb below them
        bombing_aliens =  [alien for alien_group in alien_groups for alien in alien_group.sprites()]
        for alien in bombing_aliens: 
            if (alien.bomb_active == False):
                activate_bomb = random.randint(0, 100) < bomb_frequency
                if activate_bomb and alien.bomb_active == False:
                    alien.bomb_active = True
                    newestBomb = BombSprite( 0, 0, 5, 15, .03, alien)
                    newestBomb.position = (alien.position[0] + alien.get_width()/2, \
                                           alien.position[1] + alien.get_height())
                    active_bombs.append(newestBomb)


def handle_active_bombs(active_bombs):
    bombs_to_remove = []
    for bomb in active_bombs:
        (bomb_x, bomb_y) = bomb.position
        bomb_y = bomb_y + bomb.speed
        bomb.position = (bomb_x, bomb_y)
        bomb.update()
        bomb.draw(window)
        if (bomb_y > window_height):
            bomb.parent.bomb_active = False
            bomb.position = (0, 0)
            bombs_to_remove.append(bomb)
        if (handle_player_hit(bomb_x, bomb_y)):
            bomb.parent.bomb_active = False
            bomb.position = (0, 0)
            bombs_to_remove.append(bomb)

    if (len(bombs_to_remove) > 0):
        if (len(active_bombs) > 0):
            for bomb in bombs_to_remove:
                active_bombs.remove(bomb)

########## GAME STATE HANDLING ##########
# This section of code handles game state for when we want
# to speed up the aliens
########################################
def handle_alien_speedup(total_aliens):
    global blink_speed, bomb_frequency, first_speed_up, second_speed_up, third_speed_up

    if (total_aliens() == 20):
      if first_speed_up == False:
        blink_speed = 200
        bomb_frequency = 10
        speed_up_aliens()
        first_speed_up = True
    
    if (total_aliens() == 5):
      if second_speed_up == False:
        blink_speed = 100
        bomb_frequency = 20
        speed_up_aliens()
        second_speed_up = True

    if (total_aliens() == 1):
      if third_speed_up == False:
        bomb_frequency = 40
        blink_speed = 50
        speed_up_aliens(2.0)
        third_speed_up = True

def advance_level_initialization():
    global level, alien_groups, \
      first_speed_up, second_speed_up, third_speed_up, \
      blink_speed, bomb_frequency
    level = level + 1
    first_speed_up = False
    second_speed_up = False
    third_speed_up = False
    move_aliens_right = True
    move_aliens_down = False
    blink_speed = 400
    bomb_frequency = 4 + level 
    alien_groups = []
    create_aliens()



def handle_advance_level():
    global level, alien_groups, first_speed_up, \
     second_speed_up, third_speed_up, board_cleared, \
     start_clear_delay

    if (board_cleared and pygame.time.get_ticks() - start_clear_delay > 2000):
        advance_level_initialization()
        board_cleared = False

    if (len(alien_groups) <= 0 ) and not board_cleared:
        board_cleared = True
        start_clear_delay = pygame.time.get_ticks()
       

def initialize_game_state():
    global player_score, start_time, game_over, \
        player_left, player_right, bullet_active, \
        player, alien_groups, score, player_lives,  \
        move_aliens_right, move_aliens_down, \
        first_speed_up, second_speed_up, third_speed_up, \
        level, bomb_frequency, blink_speed
    
    print("Initializing game state")
    start_time = pygame.time.get_ticks()
    player_limit = 3
    move_aliens_right = True
    move_aliens_down = False
    level = 1
    game_over = False
    first_speed_up = False
    second_speed_up = False
    third_speed_up = False
    bomb_frequency = 5
    blink_speed = 400
    player_score = 0
    player_lives = 3
    game_over = False
    player_left = False
    player_right = False
    bullet_active = False
    player.dead = False
    player.update()
    lives_indicator.update_lives(player_lives)
    create_aliens()


def total_aliens():
    global alien_groups
    total = 0
    for alien_group in alien_groups:
        total += len(alien_group)
    return total


def speed_up_aliens(factor = 1.0):
    global level
    for alien_group in alien_groups:
        for alien in alien_group:
            alien.speed = alien.speed + .01 * factor * (.9 + level/10.0)


def show_game_over_prompt():
    global game_over
    game_over = True
    game_over_message.draw(window)
    play_again_message.draw(window)


initialize_game_state()

# Main game loop
running = True
start_time = pygame.time.get_ticks()
first_speed_up = False
second_speed_up = False
third_speed_up = False
blink_speed = 400
saucer_blink_speed = 150

def handle_player_movement(window_width, player_left, player_right, player, player_x):
    if (player.dead):
        pass
    elif player_left:
        if (player_x - player.speed) > 0:
            player.move_left()
    elif player_right:
        if (player_x + player.speed) < window_width - player.get_width():
            player.move_right()

    player.update()
    player.draw(window)

def draw_aliens(window, alien_groups):
    for alien_group in alien_groups:
        for alien in alien_group.sprites():
            alien.draw(window)
            check_for_removal(alien)

def handle_scoring(window, score, player_score):
    score.score = player_score
    hi_score.update_high_score(player_score)
    lives_indicator.update()
    lives_indicator.draw(window)
    score_group.update()
    score_group.draw(window)  


while running:
    (player_x, player_y) = player.position
    window.fill(BLACK)

    running = process_events()  # process the keyboard
    
    if (game_over):
        show_game_over_prompt()
        pygame.display.flip()
        continue

    # scoring
    handle_scoring(window, score, player_score)

    # move the aliens
    handle_alien_movement()

    #launch the saucer every 20 seconds if the game is not over.
    if game_over == False and game_time % 20000 == 0 and game_time > 0:
        start_saucer()

    # handle saucer movement
    handle_saucer_movement()

    # move the player
    handle_player_movement(window_width, player_left, player_right, player, player_x)

    # move the bullet
    if bullet_active:
        bullet_active = handle_bullet(bullet, bullet_active)    


    # check for bomb activation every 2 seconds
    check_for_bomb_activation()

    # update active bombs
    handle_active_bombs(active_bombs)

    # draw the aliens and check for removal
    draw_aliens(window, alien_groups)

    
    # check if its time to speed up the aliens
    # based on the number of aliens left
    handle_alien_speedup(total_aliens)

    handle_advance_level()

    # show the display
    pygame.display.flip()

    # update the game time
    game_time = pygame.time.get_ticks() - start_time
    
