import pygame
import random
from core.app_assets import AppAssets

from core.app_colors import AppColors
from core.app_config import AppConfig


# Initialize basic pygame stuff
pygame.font.init() 
WIN = pygame.display.set_mode((AppConfig.SCREEN_WIDTH, AppConfig.SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()


class Player():
    def __init__(self, starting_x, starting_y):
        super().__init__()
        self.start_pos = [starting_x, starting_y]
        self.width = AppConfig.PLAYER_WIDTH
        self.height = AppConfig.PLAYER_HEIGHT
        self.rect = pygame.Rect(starting_x, starting_y, self.width, self.height)
        self.image = AppAssets.player
        
    def get_pygame_rect(self):
        return pygame.rect(self.pos[0], self.pos[1], self.width, self.height)

class GameView:
    def __init__(self):
        self.is_running = True
        self.player = Player(starting_x=500, starting_y=500)
        self.game_loop()
        
    def game_loop(self):
        while self.is_running:
            CLOCK.tick(AppConfig.FPS)
            
            self.handle_events()
            self.handle_pressed_keys()
            self.redraw_window()
            
    def redraw_window(self):
        WIN.fill(AppColors.WHITE)
        WIN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        pygame.display.update()
        
    def handle_events(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                self.is_running = False
            
    def handle_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            pass
        

def main():
    GameView()

        
if __name__ == "__main__":
    main()


