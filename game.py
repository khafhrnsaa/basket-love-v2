import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
BASKET_WIDTH, BASKET_HEIGHT = 80, 80
BASKET_Y = HEIGHT - 80  
BASKET_SPEED = 10
HEART_SIZE = 60  
WHITE, RED, PINK = (255, 255, 255), (255, 0, 0), (255, 182, 193)
BLACK = (0, 0, 0)
BUTTON_GREEN = (0, 200, 0)
BUTTON_RED = (200, 0, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catching Your LOVE 💖")

# Load Images
try:
    basket_img = pygame.image.load("basket.png")
    basket_img = pygame.transform.scale(basket_img, (BASKET_WIDTH, BASKET_HEIGHT))
except:
    # Create a simple basket if image not found
    basket_img = pygame.Surface((BASKET_WIDTH, BASKET_HEIGHT))
    basket_img.fill((139, 69, 19))  # Brown color

try:
    heart_img = pygame.image.load("heart.png")
    heart_img = pygame.transform.scale(heart_img, (HEART_SIZE, HEART_SIZE))
except:
    # Create a simple heart if image not found
    heart_img = pygame.Surface((HEART_SIZE, HEART_SIZE), pygame.SRCALPHA)
    pygame.draw.polygon(heart_img, RED, [
        (HEART_SIZE//2, 0),
        (HEART_SIZE, HEART_SIZE//3),
        (HEART_SIZE, HEART_SIZE),
        (HEART_SIZE//2, HEART_SIZE-10),
        (0, HEART_SIZE),
        (0, HEART_SIZE//3)
    ])

# Basket Position
basket = pygame.Rect(WIDTH // 2 - BASKET_WIDTH // 2, BASKET_Y, BASKET_WIDTH, BASKET_HEIGHT)

# List to Track Hearts
hearts = []
score = 0
font = pygame.font.Font(None, 36)
message_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 40)

# Game State
running = True
clock = pygame.time.Clock()
message_shown = False
message_y = HEIGHT // 2
message_direction = 1
game_time = 30  # 30 seconds time limit
start_time = pygame.time.get_ticks()
show_popup = False
game_over = False

# Button rectangles
yes_button = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 50, 100, 50)
no_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 50, 100, 50)

def draw_popup():
    # Darken the background
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(s, (0, 0))
    
    # Popup box
    pygame.draw.rect(screen, WHITE, (WIDTH//2 - 150, HEIGHT//2 - 100, 300, 200))
    
    # Question text
    question = message_font.render("Will you be my Valentine?", True, RED)
    screen.blit(question, (WIDTH//2 - question.get_width()//2, HEIGHT//2 - 70))
    
    # Yes button
    pygame.draw.rect(screen, BUTTON_GREEN, yes_button)
    yes_text = button_font.render("Yes", True, BLACK)
    screen.blit(yes_text, (yes_button.centerx - yes_text.get_width()//2, yes_button.centery - yes_text.get_height()//2))
    
    # No button
    pygame.draw.rect(screen, BUTTON_RED, no_button)
    no_text = button_font.render("No", True, BLACK)
    screen.blit(no_text, (no_button.centerx - no_text.get_width()//2, no_button.centery - no_text.get_height()//2))

def show_result_message(message):
    screen.fill(PINK)
    result_text = message_font.render(message, True, RED)
    screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)  # Show message for 3 seconds

while running:
    current_time = pygame.time.get_ticks()
    elapsed_seconds = (current_time - start_time) // 1000
    remaining_time = max(0, game_time - elapsed_seconds)
    
    screen.fill(PINK)  # Background Color

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if message_shown and not show_popup:
                # Check if clicked on the message
                message_text = message_font.render("Will you be my Valentine?", True, RED)
                text_rect = message_text.get_rect(center=(WIDTH // 2, message_y))
                if text_rect.collidepoint(event.pos):
                    show_popup = True
            
            if show_popup:
                # Check button clicks
                if yes_button.collidepoint(event.pos):
                    show_result_message("Yay! I love you! ❤️")
                    running = False
                elif no_button.collidepoint(event.pos):
                    show_result_message("Aww, maybe next time... 😢")
                    running = False

    if not game_over:
        # Move Basket with Mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        basket.x = mouse_x - BASKET_WIDTH // 2  # Center basket on mouse
        
        # Keep basket within screen bounds
        if basket.x < 0:
            basket.x = 0
        if basket.x > WIDTH - BASKET_WIDTH:
            basket.x = WIDTH - BASKET_WIDTH

        # Spawn Hearts at Random Intervals
        if random.randint(1, 20) == 1:
            hearts.append([random.randint(0, WIDTH - HEART_SIZE), 0, random.randint(3, 6)])  
            # Each heart has (x, y, speed)

        # Move Hearts and Check Collision
        hearts_to_remove = []
        for heart in hearts:
            heart[1] += heart[2]  # Move heart down at its own speed

            # Collision check: If the heart is inside the basket
            if heart[1] + HEART_SIZE > BASKET_Y and basket.x < heart[0] < basket.x + BASKET_WIDTH:
                score += 1  # Increment score
                hearts_to_remove.append(heart)  
            
            elif heart[1] > HEIGHT:                        
                hearts_to_remove.append(heart)

        # Remove caught or missed hearts
        for heart in hearts_to_remove:
            hearts.remove(heart)

        # Draw Hearts First (Behind Basket)
        for heart in hearts:
            screen.blit(heart_img, (heart[0], heart[1]))  

        # Draw Basket Last (Top)
        screen.blit(basket_img, (basket.x, basket.y))  

        # Score and Time
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        time_text = font.render(f"Time: {remaining_time}s", True, BLACK)
        screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

        # Check time limit
        if remaining_time <= 0:
            game_over = True
            show_result_message(f"Time's up! Score: {score}")
            running = False

        # Valentine's Message
        if score >= 10 and not message_shown:
            for _ in range(20):  # Heart shower effect 
                hearts.append([random.randint(0, WIDTH - HEART_SIZE), random.randint(-100, 0), random.randint(3, 7)])

            for _ in range(50):  # Create a heart rain effect over time
                hearts.append([random.randint(0, WIDTH - HEART_SIZE), random.randint(-200, 0), random.randint(3, 7)])

            message_shown = True  # Ensure message is displayed only once

        # Animate Floating Message
        if message_shown and not show_popup:
            message_y += message_direction
            if message_y > HEIGHT // 2 + 10 or message_y < HEIGHT // 2 - 10:
                message_direction *= -1  # Reverse direction to float up and down

            message_text = message_font.render("Will you be my Valentine?", True, RED)
            text_rect = message_text.get_rect(center=(WIDTH // 2, message_y))
            screen.blit(message_text, text_rect)
    
    # Show popup if activated
    if show_popup:
        draw_popup()

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
sys.exit()
