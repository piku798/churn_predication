import yaml
from pathlib import Path


def load_config():
    BASE_DIR = Path(__file__).resolve().parents[2]
    config_path = BASE_DIR / "config" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config