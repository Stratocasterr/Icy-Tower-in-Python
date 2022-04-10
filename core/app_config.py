from dataclasses import dataclass

@dataclass
class AppConfig():
    """A class containing all necessary variables for a game to run properly."""
    FPS: int = 60
    SCREEN_WIDTH: int = 880
    SCREEN_HEIGHT: int = 800
    FRAME_WIDTH: int = 40
    PLAYER_WIDTH: int = 20
    PLAYER_HEIGHT: int = 60
    JUMP_SPEED: int = 20
    PLATFORMS_TO_GENERATE: int = 100   # liczba 1 razowo generowanyc platform
    PLATFORM_HEIGHT: int = 25
    # Should be multiplied platform part width
    MAX_PLATFORM_WIDTH: int = 350
    DISTANCE_BETWEEN_PLATFORMS: int = 200
    PLATFORM_PART_WIDTH: int = 25
    MIN_PLATFORM_WIDTH: int = 5 * PLATFORM_PART_WIDTH
    DISTANCE_BETWEEN_LONG_PLATFORMS: int = 50

    CAMERA_START_GAME: int = 300
    CAMERA_SPEED: int = 2         
    CAMERA_ACCELERATION: int = 0.5  # losowa liczba do popr  
    CAMERA_NEXT_HEIGHT: int = 150
    
    GRAVITY: int = 1