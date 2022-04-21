from cmath import inf
import pygame
import random
from core.app_assets import AppAssets
from core.app_colors import AppColors
from core.app_config import AppConfig
from core.app_values_validator import validate_values

# Initialize basic pygame stuff
pygame.font.init()
WIN = pygame.display.set_mode((AppConfig.SCREEN_WIDTH, AppConfig.SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()


class Platform:
    def __init__(self, index):
        self.index = index

        # Scale platform assets to values provided by an AppConfig file
        self.image_left = pygame.transform.scale(AppAssets.left_platform_edge,
                                                 (AppConfig.PLATFORM_PART_WIDTH, AppConfig.PLATFORM_HEIGHT))
        self.image_middle = pygame.transform.scale(AppAssets.middle_platform_part,
                                                   (AppConfig.PLATFORM_PART_WIDTH, AppConfig.PLATFORM_HEIGHT))
        self.image_right = pygame.transform.scale(AppAssets.right_platform_edge,
                                                  (AppConfig.PLATFORM_PART_WIDTH, AppConfig.PLATFORM_HEIGHT))

        self.length = random.randrange(AppConfig.MIN_PLATFORM_WIDTH, AppConfig.MAX_PLATFORM_WIDTH,
                                       AppConfig.PLATFORM_PART_WIDTH)
        self.middle_part_quantity = (self.length - 2 * AppConfig.PLATFORM_PART_WIDTH) // AppConfig.PLATFORM_PART_WIDTH
        self.pos = self.get_initial_pos()

        self.platform_rect = pygame.Rect(self.pos[0], self.pos[1], self.length, AppConfig.PLATFORM_HEIGHT)

    def get_initial_pos(self):
        _pos_y = (
                             AppConfig.SCREEN_HEIGHT - AppConfig.PLATFORM_HEIGHT) - self.index * AppConfig.DISTANCE_BETWEEN_PLATFORMS
        return [random.randint(0, AppConfig.SCREEN_WIDTH - self.length), _pos_y]

    def draw_platform(self):
        WIN.blit(self.image_left, (self.pos[0], self.pos[1]))
        # Counts the position where the next middle part should be placed

        for index in range(1, self.middle_part_quantity + 1):
            WIN.blit(self.image_middle, (self.pos[0] + index * AppConfig.PLATFORM_PART_WIDTH, self.pos[1]))

        WIN.blit(self.image_right, (self.pos[0] + self.length - AppConfig.PLATFORM_PART_WIDTH, self.pos[1]))
        return pygame.Rect(self.pos[0], self.pos[1], self.length, AppConfig.PLATFORM_HEIGHT)


class Player:
    def __init__(self, starting_x, starting_y):
        self.start_pos = [starting_x, starting_y]
        self.width = AppConfig.PLAYER_WIDTH
        self.height = AppConfig.PLAYER_HEIGHT
        self.rect = pygame.Rect(starting_x, starting_y, self.width, self.height)
        self.image = AppAssets.player
        self.gravity = AppConfig.GRAVITY
        self.run_speed = AppConfig.RUN_SPEED
        self.jump_speed = AppConfig.JUMP_SPEED
        self.run_acceleration = AppConfig.RUN_ACCELERATION

        # Right :1 / Left :-1
        self.moving_direction = 0
        self.jump = False
        self.jump_allow = False
        self.odbijanko = False
        self.collision = False

    def get_pygame_rect(self):
        return pygame.rect(self.pos[0], self.pos[1], self.width, self.height)


class GameView:
    def __init__(self):
        self.is_running = True
        self.platforms = self.create_platforms(AppConfig.PLATFORMS_TO_GENERATE)
        self.player = Player(starting_x=400, starting_y=800)
        self.background = pygame.transform.scale(AppAssets.background, (800, 800))
        self.frame = pygame.transform.scale(AppAssets.frame, (40, 800))
        self.background_speeed = 0
        self.height = -800
        self.game_loop()


    def game_loop(self):
        while self.is_running:
            previous_y = self.player.rect.y
            CLOCK.tick(AppConfig.FPS)
            self.redraw_window()
            self.gravity()
            self.handle_events()
            self.handle_pressed_keys()
            # self.Test_Mode()
            self.Camera_movement()

            if self.player.collision == False:
                i = self.collision_detection(self.get_vertical_moving_direction(previous_y))
            else:
                self.collision_time(previous_y,i)


    def redraw_window(self):
        self.platforms_rects = []
        # self.collision_detection()
        WIN.fill(AppColors.WHITE)
        WIN.blit(self.background, (40, self.background_speeed))
        WIN.blit(self.frame, (0, self.background_speeed))
        WIN.blit(self.frame, (840, self.background_speeed))
        WIN.blit(self.background, (40, self.height + self.background_speeed))
        WIN.blit(self.frame, (0, self.height + self.background_speeed))
        WIN.blit(self.frame, (840, self.height + self.background_speeed))

        if self.background_speeed >= -self.height:
            self.background_speeed = 0

        for platform in self.platforms:
            platform.draw_platform()
            self.platforms_rects.append(platform.draw_platform())

        WIN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        pygame.display.update()

    def collision_detection(self, vertical_moving_direction):
        for i in self.platforms_rects:
            if i.colliderect(self.player.rect):
                if vertical_moving_direction == -1:
                    if abs(i.top - self.player.rect.bottom) < self.player.gravity:
                        self.player.collision = True
                        return self.platforms_rects.index(i)

            else:
                self.player.collision = False


    def collision_time(self,previous_y,i):
            if self.player.rect.x > self.platforms_rects[i].x - AppConfig.PLAYER_WIDTH and self.player.rect.x < self.platforms_rects[i].x + self.platforms_rects[i].width:
                self.player.rect.y = self.platforms_rects[i].y - self.player.height
                self.player.gravity = 0
                self.player.jump = False
            else:
                self.player.collision = False


    # Gravity
    def gravity(self):
        previous_y = self.player.rect.y

        if self.player.rect.y < AppConfig.SCREEN_HEIGHT - AppConfig.PLAYER_HEIGHT:
            self.player.rect.y += self.player.gravity

        else:
            self.player.rect.y = AppConfig.SCREEN_HEIGHT - AppConfig.PLAYER_HEIGHT
            self.player.jump = False

        if previous_y != self.player.rect.y:
            self.player.gravity += 1

        else:
            self.player.gravity = AppConfig.GRAVITY
            self.player.jump = False


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False


    def create_platforms(self, number_of_latforms):
        _platforms = []
        for platform_index in range(number_of_latforms):
            _platforms.append(Platform(platform_index))
        return _platforms


    def handle_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()

# Odbijanko

        if self.player.odbijanko:
            if self.player.jump == False:
                self.player.odbijanko = False
                self.player.jump_speed = AppConfig.JUMP_SPEED
                self.player.run_acceleration = AppConfig.RUN_ACCELERATION
            else:
                self.player.jump_speed = 1.5 * AppConfig.JUMP_SPEED
                if self.player.moving_direction == 1:
                    self.player.rect.x -= self.player.run_speed + self.player.run_acceleration
                else:
                    self.player.rect.x += self.player.run_speed + self.player.run_acceleration

                if self.player.rect.x + self.player.run_speed + self.player.run_acceleration > AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH:
                    self.player.rect.x = AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH
                    self.player.run_acceleration = AppConfig.RUN_ACCELERATION

                if self.player.rect.x - (self.player.run_speed + self.player.run_acceleration) < 0:
                    self.player.rect.x = 0
                    self.player.run_acceleration = AppConfig.RUN_ACCELERATION

# R/L moves + acceleration

        else:
            if pressed_keys[pygame.K_RIGHT]:
                if self.player.rect.x + self.player.run_speed + self.player.run_acceleration > AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH:
                    if self.player.jump and self.player.run_acceleration != AppConfig.RUN_ACCELERATION:
                        self.player.odbijanko = True
                    else:
                        self.player.rect.x = AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH
                        self.player.run_acceleration = AppConfig.RUN_ACCELERATION
                else:
                    self.player.rect.x += self.player.run_speed + self.player.run_acceleration

                if self.player.moving_direction == 1 and self.player.rect.x != AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH:
                    self.player.run_acceleration += AppConfig.RUN_ACCELERATION / 3

                else:
                    self.player.run_acceleration = AppConfig.RUN_ACCELERATION
                self.player.moving_direction = 1

            elif pressed_keys[pygame.K_LEFT]:

                if self.player.rect.x - (self.player.run_speed + self.player.run_acceleration) < 0:
                    if self.player.jump and self.player.run_acceleration != AppConfig.RUN_ACCELERATION:
                        self.player.odbijanko = True
                    else:
                        self.player.rect.x = 0
                        self.player.run_acceleration = AppConfig.RUN_ACCELERATION

                else:
                    self.player.rect.x -= self.player.run_speed + self.player.run_acceleration

                if self.player.moving_direction == -1 and self.player.rect.x != 0:
                    self.player.run_acceleration += AppConfig.RUN_ACCELERATION / 3
                else:
                    self.player.run_acceleration = AppConfig.RUN_ACCELERATION

                self.player.moving_direction = -1

#Skakanko

        if pressed_keys[pygame.K_SPACE] == False:
            self.jump_allow = True

        if pressed_keys[pygame.K_SPACE] and self.jump_allow:
            self.player.jump = True
            self.player.collision = False
            self.jump_allow = False

        if self.player.jump:
            self.player.rect.y -= self.player.jump_speed + self.player.run_acceleration / 5

        if (pressed_keys[pygame.K_RIGHT] == False and self.player.moving_direction == 1) or (
                pressed_keys[pygame.K_LEFT] == False and self.player.moving_direction == -1):
            self.player.run_acceleration = AppConfig.RUN_ACCELERATION


    def Camera_movement(self):
        camera_speed,player_y_dicrease = self.get_camera_speed()

        if self.player.rect.y < AppConfig.CAMERA_START_GAME:
            for x in range(AppConfig.PLATFORMS_TO_GENERATE):
                self.platforms[x].pos[1] += camera_speed
            self.player.rect.y += player_y_dicrease
            AppConfig.CAMERA_START_GAME = inf
            self.background_speeed += camera_speed


    def Test_Mode(self):
        if pygame.key.get_pressed()[pygame.K_c]:
            self.background_speeed += AppConfig.CHEAT_POWER
            for i in range(AppConfig.PLATFORMS_TO_GENERATE):
                self.platforms[i].pos[1] += AppConfig.CHEAT_POWER


    def get_vertical_moving_direction(self, previous_y):
        if previous_y > self.player.rect.y:
            return 1
        elif previous_y < self.player.rect.y:
            return -1
        else:
            return 0


    def get_camera_speed(self):
        camera_speed = AppConfig.CAMERA_SPEED
        player_y_dicrease = 0
        if self.player.rect.y < AppConfig.SCREEN_HEIGHT / 7 and self.player.jump:
            camera_speed = 5 * camera_speed
            player_y_dicrease = camera_speed
            self.player.jump_speed = AppConfig.JUMP_SPEED
        else:
            self.player.jump_speed = AppConfig.JUMP_SPEED

        return [camera_speed , player_y_dicrease ]


def main():
    validate_values()
    GameView()


if __name__ == "__main__":
    main()
