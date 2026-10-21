import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    rdv_host: str
    rdv_port: int
    namespace: str
    name: str
    listen_port: int
    register_ttl: int = 7200
    discover_interval: int = 20
    ping_interval: int = 30
    ping_miss_limit: int = 3
    max_reconnect_attempts: int = 5
    base_backoff: int = 2
    max_backoff: int = 60
    lives: int = 6
    max_players: int = 4
    turn_timeout: int = 30
    words_file: str = "words.txt"
    log_file: Optional[str] = None

    @property
    def peer_id(self) -> str:
        """Propriedade utilitária para obter o peer_id."""
        return f"{self.name}@{self.namespace}"

def validate_config(config: Config) -> None:
    if not (1 <= len(config.namespace) <= 64):
        raise ValueError("namespace should have between 1 and 64 characters")

    if not (1 <= len(config.name) <= 64):
        raise ValueError("name should have between 1 and 64 characters")

    if not (1 <= config.listen_port <= 65535):
        raise ValueError("listen_port should be between 1 and 65535")

    if not (1 <= config.register_ttl <= 86400):
        raise ValueError("register_ttl should be between 1 and 86400")

def load_config(file_path: str = "config.json") -> Config:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    config = Config(**data)

    # TODO sobrescrever com argumentos de linha de comando
    validate_config(config)

    return config
