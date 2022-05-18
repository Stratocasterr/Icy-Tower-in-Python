from dataclasses import dataclass
from core.app_assets import AppAssets

@dataclass
class AppConfig():
    """A class containing all necessary variables for a game to run properly."""
    FPS: int = 60
    SCREEN_WIDTH: int = 880
    SCREEN_HEIGHT: int = 800
    FRAME_WIDTH: int = 40

    PLAYER_WIDTH: int = AppAssets.player.get_width()
    PLAYER_HEIGHT: int = AppAssets.player.get_height()
    JUMP_SPEED: int = 20
    RUN_SPEED: int = 5
    RUN_ACCELERATION: int = RUN_SPEED / 5

    PLATFORMS_TO_GENERATE: int = 101  # liczba 1 razowo generowanyc platform
    PLATFORM_HEIGHT: int = 25
    # Should be multiplied platform part width
    MAX_PLATFORM_WIDTH: int = 500
    DISTANCE_BETWEEN_PLATFORMS: int = 200
    PLATFORM_PART_WIDTH: int = 25
    MIN_PLATFORM_WIDTH: int = 10 * PLATFORM_PART_WIDTH
    DISTANCE_BETWEEN_LONG_PLATFORMS: int = 50
    DISTANCE_BETWEEN_SIGNS: int = 10

    PLATFORM_SIGN_WIDTH: int = 50
    PLATFORM_SIGN_HEIGHT: int = 20

    CAMERA_START_GAME: int = 300
    CAMERA_SPEED: int = 2
    CAMERA_ACCELERATION: int = 0.5  # losowa liczba do popr
    CAMERA_NEXT_HEIGHT: int = 150
    CHEAT_POWER: int = 10
    GRAVITY: int = 1