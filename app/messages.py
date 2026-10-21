import json
from dataclasses import asdict, dataclass

from app.config_loader import Config

@dataclass
class RendezvousMessage:
    # REQUEST
    type: str | None = None
    namespace: str | None = None
    name: str | None = None
    port: int | None = None
    ttl: int | None = None

    # RESPONSE
    status: str | None = None
    message: str | None = None
    ip: str | None = None
    peers: list[dict] | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

    def to_json(self) -> str:
        return json.dumps(self.to_dict()) + "\n"

    @classmethod
    def from_dict(cls, data: dict) -> RendezvousMessage:
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    @classmethod
    def build_register(cls, config: Config) -> RendezvousMessage:
        return cls(type="REGISTER", 
                   namespace=config.namespace,
                   name=config.name,
                   port=config.listen_port,
                   ttl=config.register_ttl)   

