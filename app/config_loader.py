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


def load_config(file_path: str = "config.json") -> Config:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Config(**data)
