import pygame

class AppAssets: #"D:\Python_programy\Icy_Tower\Icy-Tower-in-Python\assets"
    """Import all needed assets here."""
    '''player = pygame.image.load("D:/Python_programy/Icy_Tower/Icy-Tower-in-Python/assets/player.png")     # zostawcie mi te sciezki bo nie chce mi sie co wersje je dodawac J
    left_platform_edge = pygame.image.load("D:/Python_programy/Icy_Tower/Icy-Tower-in-Python/assets/left_platform_edge.png")
    middle_platform_part = pygame.image.load("D:/Python_programy/Icy_Tower/Icy-Tower-in-Python/assets/middle_platform_part.png")
    right_platform_edge = pygame.image.load("D:/Python_programy/Icy_Tower/Icy-Tower-in-Python/assets/right_platform_edge.png")
    start_platform = pygame.image.load("D:/Python_programy/Icy_Tower/Icy-Tower-in-Python/assets/start_platform.png")
    background = pygame.image.load("D:/Python_programy/Icy_Tower/Icy-Tower-in-Python/assets/background.png")
    frame = pygame.image.load("D:/Python_programy/Icy_Tower/Icy-Tower-in-Python/assets/Frame.png")'''

    player = pygame.image.load("assets/player1.png")

    left_platform_edge = pygame.image.load("assets/left_platform_edge.png")
    middle_platform_part = pygame.image.load("assets/middle_platform_part.png")
    right_platform_edge = pygame.image.load("assets/right_platform_edge.png")
    start_platform = pygame.image.load("assets/start_platform.png")


    background = pygame.image.load("assets/background.jpg")
    frame = pygame.image.load("assets/frame1.png")
    platform_sign = pygame.image.load("assets/platform_sign.png")  # jacek dodaj sobie to
    main_menu_pic = pygame.image.load("assets/menu.png")
    main_start_but = pygame.image.load("assets/menu_start_game.png")
    main_help_but = pygame.image.load("assets/menu_help.png")
    main_quit_but = pygame.image.load("assets/menu_quit.png")

    game_is_over_pic = pygame.image.load("assets/game_is_over_pic.png")
    game_is_over_backtomain_pic = pygame.image.load("assets/game_is_over_comeback_pic.png")
    game_is_over_tryagain_pic = pygame.image.load("assets/game_is_over_try_again_pic.png")