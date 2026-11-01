import time


class Peer:
    def __init__(
        self, ip: str, port: int, name: str, namespace: str, ttl: int, expires_in: int
    ) -> None:
        self.addr: tuple[str, int] = (ip, port)
        self.name = name
        self.namespace = namespace
        self.ttl = ttl
        self.expire_at = time.perf_counter() + expires_in

    def __repr__(self) -> str:
        return f"{self.name}@{self.namespace} ({self.addr[0]}:{self.addr[1]})"

    @property
    def is_expired(self) -> bool:
        return time.perf_counter() >= self.expire_at

    @property
    def peer_id(self):
        return f"{self.name}@{self.namespace}"

    @staticmethod
    def from_dict(d):
        ip = d.get("ip")
        port = d.get("port")
        name = d.get("name")
        namespace = d.get("namespace")
        ttl = d.get("ttl")
        expires_in = d.get("expires_in")

        return Peer(ip, port, name, namespace, ttl, expires_in)
