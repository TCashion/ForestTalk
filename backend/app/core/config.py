from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "ForestTalk API"
    frontend_origin: str = "http://127.0.0.1:5173"


settings = Settings()
