import pygame
import random
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 1200
HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
WHITE_2 = (180, 180, 180)
WHITE_3 = (150, 150, 150)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Player settings
PLAYER_SIZE = 50
PLAYER_COLOR = RED
PLAYER_SPEED = 6

# Enemy settings
ENEMY_SIZE = 20
ENEMY_COLOR = WHITE

# Score settings
SCORE_FONT_SIZE = 24

# Function to calculate Euclidean distance
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to generate a random enemy position
def generate_random_enemy_position(min_position, max_position):
    return random.randint(min_position, max_position)

# Function to generate a random delay for the enemy to reappear
def generate_random_delay():
    return random.uniform(1, 3)

# Function to calculate points on the Lemniscate of Gerono
def gerono_lemniscate(a, num_points):
    points = []
    for t in range(num_points):
        angle = t * 2 * math.pi / num_points
        y = a * math.cos(angle) * 1.4
        x = a * math.sin(2 * angle) * 1.4
        points.append((x, y))
    return points

# Function to handle the game
def main():
    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Following point")

    # Set up clock
    clock = pygame.time.Clock()

    # Initialize player position
    player_x = WIDTH // 2
    controlled_point = [WIDTH // 2, HEIGHT - 50]

    # Initialize enemy position
    enemy_x = random.randint(0, WIDTH)
    enemy_visible = True  
    last_touch_time = None
    nb_touched = 0

    # Initialize score
    score = 0

    # Parameters for Lemniscate of Gerono
    a = 200
    num_points = 120
    current_point = 0
    update_position = 0

    # Bar 1 dimensions and position
    bar_width = WIDTH - 10
    bar_height = 2
    bar_x = 5
    bar_y = HEIGHT // 6

    # Bar 2 position
    bar_y2 = HEIGHT // 23

    # Wait for Space key to start game loop
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            waiting = False

    # Define 4 sessions
    for i in range(1, 5):
        # Define a timer
        t_session = time.time()

        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Fill the screen
            screen.fill(BLACK)

            # Get the keyboard keys
            keys = pygame.key.get_pressed()

            # Pass the current step
            if keys[pygame.K_ESCAPE]:
                    time.sleep(3)
                    break

            if i in {1,3,4}:
                # Move player
                if keys[pygame.K_q] and player_x >= 5:
                    player_x -= PLAYER_SPEED
                if keys[pygame.K_d] and player_x <= WIDTH - PLAYER_SIZE - 5:
                    player_x += PLAYER_SPEED

                # If the enemy is not visible and enough time has passed, make it reappear
                if not enemy_visible and last_touch_time is not None and time.time() - last_touch_time >= generate_random_delay():
                    enemy_x = generate_random_enemy_position(10 + PLAYER_SIZE, WIDTH - (10 + PLAYER_SIZE))
                    enemy_visible = True
                    nb_touched = 0

                # Calculate distance between player and enemy
                distance = calculate_distance((player_x + PLAYER_SIZE // 2 + 1, HEIGHT // 10), (enemy_x, HEIGHT // 10))

                # Reward the player based on proximity to enemy
                if distance <= 10 and enemy_visible:
                    nb_touched += 1
                    if nb_touched >= 30:
                        enemy_visible = False
                        score += int((100 - distance))
                        last_touch_time = time.time()                   

                # Draw the player
                pygame.draw.rect(screen, PLAYER_COLOR, pygame.Rect(player_x, HEIGHT // 10 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE),  2)

                if enemy_visible:
                    # Draw the enemy
                    pygame.draw.circle(screen, ENEMY_COLOR, (enemy_x, HEIGHT // 10), ENEMY_SIZE // 2)

            if i in {2,3,4}:
                # Move player
                if keys[pygame.K_UP]:
                    controlled_point[1] -= PLAYER_SPEED
                if keys[pygame.K_DOWN]:
                    controlled_point[1] += PLAYER_SPEED
                if keys[pygame.K_LEFT]:
                    controlled_point[0] -= PLAYER_SPEED
                if keys[pygame.K_RIGHT]:
                    controlled_point[0] += PLAYER_SPEED

                # Generate points on the Lemniscate of Gerono
                points = gerono_lemniscate(a, num_points)

                # Draw the whole Lemniscate of Gerono
                #for point in points:
                #    pygame.draw.circle(screen, WHITE, (int(WIDTH // 2 + point[0]), int(HEIGHT // 1.7 + point[1])), 4)

                # Draw a few points of Lemniscate of Gerono
                if current_point == 0:
                    pygame.draw.circle(screen, WHITE, (int(WIDTH // 2 + points[current_point][0]), int(HEIGHT // 1.7 + points[current_point][1])), 4)
                elif current_point == 1:
                    pygame.draw.circle(screen, WHITE_2, (int(WIDTH // 2 + points[current_point-1][0]), int(HEIGHT // 1.7 + points[current_point-1][1])), 4)
                    pygame.draw.circle(screen, WHITE, (int(WIDTH // 2 + points[current_point][0]), int(HEIGHT // 1.7 + points[current_point][1])), 4)
                else:
                    pygame.draw.circle(screen, WHITE_3, (int(WIDTH // 2 + points[current_point-2][0]), int(HEIGHT // 1.7 + points[current_point-2][1])), 4)
                    pygame.draw.circle(screen, WHITE_2, (int(WIDTH // 2 + points[current_point-1][0]), int(HEIGHT // 1.7 + points[current_point-1][1])), 4)
                    pygame.draw.circle(screen, WHITE, (int(WIDTH // 2 + points[current_point][0]), int(HEIGHT // 1.7 + points[current_point][1])), 4)
                
                # Draw the controlled point
                pygame.draw.circle(screen, RED, (int(controlled_point[0]), int(controlled_point[1])), 5)

                # Increment current_point for next frame
                if  update_position == 24:
                    current_point += 1
                    if current_point >= len(points):
                        current_point = 0
                    update_position = 0
                else:
                    update_position += 1

                # Calculate distance between player and enemy
                distance_curve = calculate_distance((controlled_point[0], controlled_point[1]), ((WIDTH // 2 + points[current_point][0]), (HEIGHT // 1.7 + points[current_point][1])))

                # Reward the player based on proximity to enemy
                if distance_curve <= 10:
                    score += int((100 - distance_curve)*0.02)    

            # Draw the horizontal bar 1
            pygame.draw.rect(screen, WHITE, pygame.Rect(bar_x, bar_y, bar_width, bar_height))

            # Draw the horizontal bar 2
            pygame.draw.rect(screen, WHITE, pygame.Rect(bar_x, bar_y2, bar_width, bar_height))

            # Timer 
            timer = 52 - (time.time() - t_session)

            # Display score and timer
            font = pygame.font.Font(None, SCORE_FONT_SIZE)
            score_text = font.render("Score: " + str(score), True, WHITE)
            screen.blit(score_text, (10, 5))
            timer_game = font.render("Temps restant: " + "%.0f" % timer, True, WHITE)
            screen.blit(timer_game, (200, 5))
            step_game = font.render("Epreuve: " + str(i), True, WHITE)
            screen.blit(step_game, (600, 5))

            # Cap the frame rate
            clock.tick(60)

            # If step is over and game not
            if timer <= 0 and i != 4:
                # Fill the screen
                screen.fill(BLACK)

                # Print the time before the next step
                inter_game = font.render("Prochaine épreuve dans " + "%.0f" % (timer + 20) + " secondes", True, WHITE)
                screen.blit(inter_game, (WIDTH // 2 -140, HEIGHT // 2))

                # If timebreak over
                if timer <= -20:
                    break

            # If step is over and game over too
            elif timer <= 0 and i == 4: 
                # Fill the screen
                screen.fill(BLACK)

                # Print the score
                score_text = font.render("Score: " + str(score), True, WHITE)
                screen.blit(score_text, (WIDTH // 2 -50, HEIGHT // 2))

                # If game is over
                if timer <= -10:
                    break
            
            # Update the display
            pygame.display.flip()

            # Introduce a delay and pump the event queue
            pygame.time.delay(20)
            pygame.event.pump()

if __name__ == "__main__":
    main()
