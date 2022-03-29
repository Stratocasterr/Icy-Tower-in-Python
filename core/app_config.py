from dataclasses import dataclass

@dataclass
class AppConfig():
    """A class containing all necessary variables for a game to run properly."""
    FPS: int = 60
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 800
    PLAYER_WIDTH: int = 20
    PLAYER_HEIGHT: int = 60
    
    PLATFORM_HEIGHT: int = 25
    # Should be multiplied platform part width
    MAX_PLATFORM_WIDTH: int = 250
    DISTANCE_BETWEEN_PLATFORMS: int = 75
    PLATFORM_PART_WIDTH: int = 25
    MIN_PLATFORM_WIDTH: int = 3 * PLATFORM_PART_WIDTH

    GRAVITY: int = 1