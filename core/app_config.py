from dataclasses import dataclass

@dataclass
class AppConfig():
    """A class containing all necessary variables for a game to run properly."""
    FPS: int = 60
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 800
    PLAYER_WIDTH: int = 20
    PLAYER_HEIGHT: int = 60


