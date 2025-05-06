import pygame
import sys
from screeninfo import get_monitors

# Pygame initialization
pygame.init()
monitor = get_monitors()[0]
WIDTH, HEIGHT = 700, monitor.height - 100
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Thrust Simulation")
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
RED = (200, 50, 50)

# Ground setup
GROUND_HEIGHT = 100

# Slider setup
SLIDER_X = WIDTH - 50
SLIDER_Y = 100
SLIDER_HEIGHT = HEIGHT - GROUND_HEIGHT - SLIDER_Y - 20
SLIDER_WIDTH = 10
KNOB_RADIUS = 15  

if __name__ == "__main__":
    pos, vel = 0, 0
    thrust = 0  # Start value
    fuel = 100  # Fuel amount
    gravity = 50 # Gravity constant
    dragging = False

    running = True

    with open("highscore.txt", "r") as f:
        high_score = f.read()
        if high_score == "":
            high_score = 0
        else:
            high_score = float(high_score)

    while running: # Main loop
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                knob_y = SLIDER_Y + SLIDER_HEIGHT - (thrust / 100) * SLIDER_HEIGHT
                knob_x = SLIDER_X + SLIDER_WIDTH // 2
                if (mx - knob_x)**2 + (my - knob_y)**2 <= KNOB_RADIUS**2:
                    dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                my = pygame.mouse.get_pos()[1]
                rel_y = max(SLIDER_Y, min(my, SLIDER_Y + SLIDER_HEIGHT))
                thrust = 100 * (SLIDER_Y + SLIDER_HEIGHT - rel_y) / SLIDER_HEIGHT

        # Physics 
        if fuel > 0:
            fuel -= (thrust / 20) * (1/FPS)
        else:
            thrust = 0
            fuel = 0

        # Update position and velocity
        vel += (thrust) * (1/FPS)
        vel -= gravity * (1/FPS)

        pos += vel * (1/FPS)

        # Check for ground collision`
        if pos < 0:
            pos = 0
            vel = 0

        if vel <= 0 and fuel == 0:
            if pos > high_score:
                high_score = pos
                text = font.render("NEW HIGH SCORE!", True, WHITE)
                screen.blit(text, (WIDTH // 2, HEIGHT // 2))
        text = font.render("Press space to reset", True, WHITE)
        screen.blit(text, (WIDTH // 2, HEIGHT // 2 - 20))
            

        # Draw background
        for y in range(HEIGHT - GROUND_HEIGHT):
            ratio = y / (HEIGHT - GROUND_HEIGHT)
            r = int(SKY_BLUE[0] * ratio)
            g = int(SKY_BLUE[1] * ratio)
            b = int(SKY_BLUE[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # Draw slider
        pygame.draw.rect(screen, GREY, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))
        
        # Calculate knob position
        knob_y = SLIDER_Y + SLIDER_HEIGHT - (thrust / 100) * SLIDER_HEIGHT
        knob_x = SLIDER_X + SLIDER_WIDTH // 2
        
        # Draw knob
        pygame.draw.circle(screen, RED, (knob_x, int(knob_y)), KNOB_RADIUS)

        # Draw rocket
        pygame.draw.circle(screen, RED, (WIDTH // 2, int(HEIGHT - GROUND_HEIGHT - (pos / 20))), 10)

        # Draw fuel bar
        FUEL_BAR_X = 40
        FUEL_BAR_Y = SLIDER_Y
        FUEL_BAR_WIDTH = 20
        FUEL_BAR_HEIGHT = SLIDER_HEIGHT
        fuel_percent = fuel / 100
        fuel_height = FUEL_BAR_HEIGHT * fuel_percent
        pygame.draw.rect(screen, GREY, (FUEL_BAR_X, FUEL_BAR_Y, FUEL_BAR_WIDTH, FUEL_BAR_HEIGHT))  # Background
        pygame.draw.rect(screen, RED, (FUEL_BAR_X, FUEL_BAR_Y + (FUEL_BAR_HEIGHT - fuel_height), FUEL_BAR_WIDTH, fuel_height))  # Fuel


        # Draw values (after background)
        font = pygame.font.SysFont(None, 28)
        text = font.render(f"Position: {int(pos)}", True, WHITE)
        screen.blit(text, (SLIDER_X - 100, SLIDER_Y - 80))
        text = font.render(f"Velocity: {int(vel)}", True, WHITE)
        screen.blit(text, (SLIDER_X - 100, SLIDER_Y - 60))
        text = font.render(f"Thrust: {int(thrust)}", True, WHITE)
        screen.blit(text, (SLIDER_X - 100, SLIDER_Y - 40))

        text = font.render(f"High Score: {int(high_score)}", True, WHITE)
        screen.blit(text, (FUEL_BAR_X, FUEL_BAR_Y - 40))

        pygame.display.flip()
        clock.tick(FPS)

# Write high score to file
with open("highscore.txt", "w") as f:
    f.write(str(pos))

pygame.quit()