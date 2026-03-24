from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = "ForestTalk API"
    frontend_origin: str = "http://127.0.0.1:5173"
    backend_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parents[2]
    )
    uploads_dir: Path = field(init=False)
    outputs_dir: Path = field(init=False)
    outputs_url_path: str = "/outputs"

    def __post_init__(self) -> None:
        object.__setattr__(self, "uploads_dir", self.backend_root / "uploads")
        object.__setattr__(self, "outputs_dir", self.backend_root / "outputs")


settings = Settings()
