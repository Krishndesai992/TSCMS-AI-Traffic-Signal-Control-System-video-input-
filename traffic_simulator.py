# simulation/traffic_simulator.py

import pygame
import config
from modules.signal_controller import SignalController

# Window dimensions from config
WIDTH = config.WINDOW_WIDTH
HEIGHT = config.WINDOW_HEIGHT

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSCMS - Traffic Signal Simulation")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont(None, 32)

    controller = SignalController()

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        controller.update()

        current_lane = controller.get_current_lane()
        state = controller.get_state()
        timer = controller.get_timer()

        lanes = ["North", "East", "South", "West"]
        
        # Only numbers as labels
        lane_numbers = {
            "North": "1",
            "East": "2",
            "South": "3",
            "West": "4"
        }

        positions = {
            "North": (WIDTH // 2, 100),
            "East": (WIDTH - 150, HEIGHT // 2),
            "South": (WIDTH // 2, HEIGHT - 100),
            "West": (150, HEIGHT // 2),
        }

        for lane in lanes:
            x, y = positions[lane]
            
            if lane == current_lane:
                if state == "GREEN":
                    color = GREEN
                elif state == "YELLOW":
                    color = YELLOW
            else:
                color = RED

            pygame.draw.circle(screen, color, (x, y), 40)
            
            # Draw only lane number
            text = font.render(lane_numbers[lane], True, WHITE)
            screen.blit(text, (x - 10, y - 70))

        # Timer (Top Left)
        timer_text = font.render(f"Timer: {timer}", True, WHITE)
        screen.blit(timer_text, (20, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()