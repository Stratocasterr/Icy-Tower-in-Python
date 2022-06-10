from cmath import inf
import pygame
import random
from core.app_assets import AppAssets
from core.app_colors import AppColors
from core.app_config import AppConfig
from core.app_values_validator import validate_values
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', AppConfig.PLATFORM_SIGN_HEIGHT)
score_font = pygame.font.SysFont('comicsans', 20, True)

# Initialize basic pygame stuff
pygame.font.init()
WIN = pygame.display.set_mode((AppConfig.SCREEN_WIDTH, AppConfig.SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

PLATFORMS_SIZE_DICT = {
        # PLATFORM_INDEX: (MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH)
        0: (AppConfig.PLATFORM_PART_WIDTH * 10, AppConfig.PLATFORM_PART_WIDTH * 15),
        1: (AppConfig.PLATFORM_PART_WIDTH * 6, AppConfig.PLATFORM_PART_WIDTH * 10),
        2: (AppConfig.PLATFORM_PART_WIDTH * 3, AppConfig.PLATFORM_PART_WIDTH * 5),
    }


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
        self.image_sign = pygame.transform.scale(AppAssets.platform_sign,
                                                 (AppConfig.PLATFORM_SIGN_WIDTH, AppConfig.PLATFORM_SIGN_HEIGHT))

        self.length = self.get_length()
        self.middle_part_quantity = (self.length - 2 * AppConfig.PLATFORM_PART_WIDTH) // AppConfig.PLATFORM_PART_WIDTH
        self.pos = self.get_initial_pos()
        self.platform_rect = pygame.Rect(self.pos[0], self.pos[1], self.length, AppConfig.PLATFORM_HEIGHT)

    def get_initial_pos(self):
        _pos_y = (
                             AppConfig.SCREEN_HEIGHT - AppConfig.PLATFORM_HEIGHT) - self.index * AppConfig.DISTANCE_BETWEEN_PLATFORMS
        return [random.randint(AppConfig.FRAME_WIDTH, AppConfig.SCREEN_WIDTH - self.length - AppConfig.FRAME_WIDTH),
                _pos_y]

    def draw_platform(self):
        # Draws the left edge of the platform
        WIN.blit(self.image_left, (self.pos[0], self.pos[1]))

        # Counts the position where the next middle part should be placed and draws them
        for index in range(1, self.middle_part_quantity + 1):
            WIN.blit(self.image_middle, (self.pos[0] + index * AppConfig.PLATFORM_PART_WIDTH, self.pos[1]))

        # Draws the right edge of the platform
        WIN.blit(self.image_right, (self.pos[0] + self.length - AppConfig.PLATFORM_PART_WIDTH, self.pos[1]))

        self.draw_sign()

        return pygame.Rect(self.pos[0], self.pos[1], self.length, AppConfig.PLATFORM_HEIGHT)

    def draw_sign(self):

        # Draw the sign on every N platform with the platform index
        if self.index % AppConfig.DISTANCE_BETWEEN_SIGNS == 0 and self.index > 0:
            _platform_sign_pos_x = self.pos[0] + (self.length - AppConfig.PLATFORM_SIGN_WIDTH) // 2
            _platform_sign_pos_y = self.pos[1] + (AppConfig.PLATFORM_HEIGHT - AppConfig.PLATFORM_SIGN_HEIGHT) / 2

            platform_sign_text = font.render(str(self.index), True, AppColors.WHITE)
            _platform_sign_text_pos_x = _platform_sign_pos_x + (
                        AppConfig.PLATFORM_SIGN_WIDTH - platform_sign_text.get_width()) // 2

            WIN.blit(self.image_sign, (_platform_sign_pos_x, _platform_sign_pos_y))
            WIN.blit(platform_sign_text, (_platform_sign_text_pos_x, _platform_sign_pos_y))

    def get_length(self):
        if self.index % AppConfig.DISTANCE_BETWEEN_LONG_PLATFORMS == 0:
            return AppConfig.SCREEN_WIDTH - 2 * AppConfig.FRAME_WIDTH
        else:
            return random.randrange(PLATFORMS_SIZE_DICT[self.index // 100][0], PLATFORMS_SIZE_DICT[self.index // 100][1],
                                    AppConfig.PLATFORM_PART_WIDTH)


class Player:
    def __init__(self, starting_x, starting_y):
        self.start_pos = [starting_x, starting_y]

        self.image = AppAssets.player
        self.width = AppConfig.PLAYER_WIDTH
        self.height = AppConfig.PLAYER_HEIGHT

        self.rect = pygame.Rect(starting_x, starting_y, self.width, self.height)

        self.gravity = AppConfig.GRAVITY
        self.run_speed = AppConfig.RUN_SPEED
        self.jump_speed = AppConfig.JUMP_SPEED
        self.run_acceleration = AppConfig.RUN_ACCELERATION

        # Right :1 / Left :-1
        self.moving_direction = 0
        self.stays = True
        self.jump = False
        self.jump_allow = False
        self.odbijanko = False
        self.collision = False

    def get_pygame_rect(self):
        return pygame.rect(self.pos[0], self.pos[1], self.width, self.height)


class GameView:
    def __init__(self):

        self.is_running = True
        self.game_is_running = True
        self.game_menu = True
        self.game_is_over = False

        self.platforms = self.create_platforms(AppConfig.PLATFORMS_TO_GENERATE)
        self.player = Player(starting_x = AppConfig.SCREEN_WIDTH // 2 , starting_y = AppConfig.SCREEN_HEIGHT - AppConfig.PLAYER_HEIGHT - AppConfig.PLATFORM_HEIGHT)
        self.background = pygame.transform.scale(AppAssets.background, (800, 800))
        self.frame = pygame.transform.scale(AppAssets.frame, (40, 800))
        self.frame_1 = pygame.transform.scale(AppAssets.frame_1, (40, 800))
        self.background_speeed = 0
        self.height = -800
        self.game_is_over_pic = AppAssets.game_is_over_pic
        self.score = 0
        self.best_score = 0
        self.timer = 0
        self.camera_speed_factor = 1
        

        self.main_menu_image = AppAssets.main_menu_image
        self.main_start_button = AppAssets.main_start_button
        self.main_quit_button = AppAssets.main_quit_button


        self.gameover_pic = AppAssets.game_is_over_pic
        self.gameover_backtomenu_but = AppAssets.game_is_over_backtomain_pic
        self.gameover_tryagain_but = AppAssets.game_is_over_tryagain_pic

        self.game_loop()


    def game_loop(self):

        while self.is_running:
            if self.game_menu:
                self.main_menu()

            elif self.game_is_running:
                previous_y = self.player.rect.y
                CLOCK.tick(AppConfig.FPS)
                self.handle_timer()
                self.redraw_window()
                self.gravity()
                self.handle_events()
                self.handle_pressed_keys()
                # self.test_mode()
                self.Camera_movement()

                if self.player.collision == False:
                    i = self.collision_detection(self.get_vertical_moving_direction(previous_y))
                else:
                    self.collision_time(previous_y,i)


            elif self.player.game_is_over:
                self.gameower_menu()


    def handle_timer(self):
        self.timer += 1
        if self.timer > 300:
            self.timer = 0
            self.camera_speed_factor += 0.1


    def redraw_window(self):
        self.platforms_rects = []
        # self.collision_detection()
        WIN.fill(AppColors.WHITE)
        WIN.blit(self.background, (40, self.background_speeed))
        WIN.blit(self.frame_1, (0, self.background_speeed))
        WIN.blit(self.frame, (840, self.background_speeed))
        WIN.blit(self.background, (40, self.height + self.background_speeed))
        WIN.blit(self.frame_1, (0, self.height + self.background_speeed))
        WIN.blit(self.frame, (840, self.height + self.background_speeed))

        if self.background_speeed >= -self.height:
            self.background_speeed = 0

        for platform in self.platforms:
            platform.draw_platform()
            self.platforms_rects.append(platform.draw_platform())


        WIN.blit(self.choose_player_image(), (self.player.rect.x, self.player.rect.y))
        self.draw_score()
        
    
        pygame.display.update()

    def draw_score(self):
        WIN.blit(AppAssets.score_bar, (AppConfig.SCREEN_WIDTH * 0.01, AppConfig.SCREEN_HEIGHT * 0.01))

        self.calculate_score()

        font = pygame.font.SysFont('comicsans', 20, True)
        score_text = font.render('Score: ' + str(self.score), True, AppColors.WHITE)
        WIN.blit(score_text, (AppConfig.SCREEN_WIDTH * 0.05, AppConfig.SCREEN_HEIGHT * 0.025))

    def calculate_score(self):
        platform_passed = 0
        for platform in self.platforms:
            if platform.pos[1] > self.player.rect.y:
                platform_passed += 1
        self.score = platform_passed * 10
            

    def choose_player_image(self):
        if not self.player.stays:
            if self.player.moving_direction == -1 : return AppAssets.player_left
            elif self.player.moving_direction == 1: return AppAssets.player_right
        else: return AppAssets.player

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
            if self.player.rect.x > self.platforms_rects[i].x - self.player.width and self.player.rect.x < self.platforms_rects[i].x + self.platforms_rects[i].width:
                self.player.rect.y = self.platforms_rects[i].y - self.player.height
                self.player.gravity = 0
                self.player.jump = False
            else:
                self.player.collision = False


    # Gravity
    def gravity(self):
        previous_y = self.player.rect.y

        if self.player.rect.y < AppConfig.SCREEN_HEIGHT :
            self.player.rect.y += self.player.gravity

        else:
            #self.player.rect.y = AppConfig.SCREEN_HEIGHT - self.player.height
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


    def create_platforms(self, number_of_platforms):
        _platforms = []
        for platform_index in range(number_of_platforms):
            _platforms.append(Platform(platform_index))
        return _platforms


    def handle_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()

# Odbijanko
        previous_x = self.player.rect.x
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

                if self.player.rect.x + self.player.run_speed + self.player.run_acceleration > AppConfig.SCREEN_WIDTH - self.player.width:
                    self.player.rect.x = AppConfig.SCREEN_WIDTH - self.player.width
                    self.player.run_acceleration = AppConfig.RUN_ACCELERATION

                if self.player.rect.x - (self.player.run_speed + self.player.run_acceleration) < 0:
                    self.player.rect.x = 0
                    self.player.run_acceleration = AppConfig.RUN_ACCELERATION

# R/L moves + acceleration



        else:
            if pressed_keys[pygame.K_RIGHT]:
                if self.player.rect.x + self.player.run_speed + self.player.run_acceleration > AppConfig.SCREEN_WIDTH - self.player.width:
                    if self.player.jump and self.player.run_acceleration != AppConfig.RUN_ACCELERATION:
                        self.player.odbijanko = True
                    else:
                        self.player.rect.x = AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH
                        self.player.run_acceleration = AppConfig.RUN_ACCELERATION
                else:
                    self.player.rect.x += self.player.run_speed + self.player.run_acceleration

                if self.player.moving_direction == 1 and self.player.rect.x != AppConfig.SCREEN_WIDTH - self.player.width:
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

        if previous_x == self.player.rect.x: self.player.stays = True
        else: self.player.stays = False


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
            self.game_over_time()
            for x in range(AppConfig.PLATFORMS_TO_GENERATE):
                self.platforms[x].pos[1] += camera_speed * self.camera_speed_factor
            self.player.rect.y += player_y_dicrease
            AppConfig.CAMERA_START_GAME = inf
            self.background_speeed += camera_speed


    def test_mode(self):
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


    def main_menu(self):

        picture = self.main_menu_images()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:
                if picture == self.main_start_button:
                    self.game_is_running = True
                    self.game_menu = False
                elif picture == self.main_quit_button:
                    self.is_running = False
                    self.game_menu = False
                else:
                    pass

        WIN.fill(AppColors.BLACK)
        WIN.blit(picture, ((AppConfig.SCREEN_WIDTH - self.main_menu_image.get_width()) // 2, 0))
        pygame.display.update()


    def main_menu_images(self):

        # staRtgamebutton


        if pygame.mouse.get_pos()[0] >= 310 and pygame.mouse.get_pos()[0] <= 544 and pygame.mouse.get_pos()[
            1] >= 352 and pygame.mouse.get_pos()[1] <= 410:
            picture = self.main_start_button



        # quitbuttom

        elif pygame.mouse.get_pos()[0] >= 308 and pygame.mouse.get_pos()[0] <= 540 and pygame.mouse.get_pos()[
            1] >= 550 and pygame.mouse.get_pos()[1] <= 586:
            picture = self.main_quit_button

        else:
            picture = self.main_menu_image

        return picture


    def game_over_time(self):
        if self.player.rect.y > AppConfig.SCREEN_HEIGHT:
            self.game_is_running = False
            self.player.game_is_over = True


    def gameower_menu(self):

        picture = self.game_over_menu_pics()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:

                if picture == self.gameover_tryagain_but:
                    self.player.game_is_over = False
                    self.game_is_running = True
                    self.restart_game()

                elif picture == self.gameover_backtomenu_but:
                    self.player.game_is_over = False
                    self.game_menu = True
                    self.restart_game()

        WIN.blit(picture, (AppConfig.SCREEN_WIDTH // 2 - self.game_is_over_pic.get_width() // 2,
                           AppConfig.SCREEN_HEIGHT // 2 - self.game_is_over_pic.get_height() // 2))
                           
        # show score on game over screen
        score_text = score_font.render(str(self.score), True, AppColors.WHITE)
        WIN.blit(score_text, (AppConfig.SCREEN_WIDTH * 0.5, AppConfig.SCREEN_HEIGHT * 0.49))
        self.check_if_best_score()
        best_score_text = score_font.render(str(self.best_score), True, AppColors.WHITE)
        WIN.blit(best_score_text, (AppConfig.SCREEN_WIDTH * 0.55, AppConfig.SCREEN_HEIGHT * 0.52))
        pygame.display.update()


    def game_over_menu_pics(self):

        if pygame.mouse.get_pos()[0] >= 357 and pygame.mouse.get_pos()[0] <= 437 and pygame.mouse.get_pos()[1] >= 488 and pygame.mouse.get_pos()[1] <= 505:
            return self.gameover_tryagain_but

        # helpbuttom

        elif pygame.mouse.get_pos()[0] >= 356 and pygame.mouse.get_pos()[0] <= 535 and pygame.mouse.get_pos()[
            1] >= 529 and pygame.mouse.get_pos()[1] <= 538:
            return self.gameover_backtomenu_but

        else: return self.gameover_pic

    def check_if_best_score(self):
        if self.score > self.best_score:
            self.best_score = self.score


    def restart_game(self):
        self.player.rect[0] = AppConfig.SCREEN_WIDTH // 2
        self.player.rect[1] = AppConfig.SCREEN_HEIGHT - AppConfig.PLAYER_HEIGHT - AppConfig.PLATFORM_HEIGHT
        self.platforms = self.create_platforms(AppConfig.PLATFORMS_TO_GENERATE)
        AppConfig.CAMERA_START_GAME = 300
        


def main():
    validate_values()
    GameView()


if __name__ == "__main__":
    main()
