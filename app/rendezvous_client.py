import json
import logging
import socket

from app.config_loader import Config, RDVServer
from app.messages import RendezvousMessage
from app.peer import Peer

logger = logging.getLogger(__name__)

MAX_MESSAGE_LEN_BYTES = 32 * 1024  # 32 KB


def exchange_message(
    server: RDVServer, message: RendezvousMessage
) -> RendezvousMessage:
    if not message.type:
        raise ValueError(
            "Mensagem precisa ser de um tipo (REGISTER / UNREGISTER / DISCOVER / REFRESH)"
        )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server)

        message_encoded = message.to_json().encode()

        sock.sendall(message_encoded)
        logger.debug(f"Sent {message.type}:\n {message.to_json()}")

        response_bytes = sock.recv(MAX_MESSAGE_LEN_BYTES)
        if not response_bytes:
            raise RuntimeError("Empty response from Rendezvous server")

        response_dict = json.loads(response_bytes.decode("utf-8"))

        logger.debug(f"Received :\n {response_dict}")
        return RendezvousMessage.from_dict(response_dict)


def register(config: Config) -> tuple[str, int] | None:
    server = config.rdv_server
    message = RendezvousMessage.build_register(config)
    response = exchange_message(server, message)

    if response.is_ok():
        if not response.ip or not response.ttl:
            raise RuntimeError("REGISTER OK but no info returned (expected ip and ttl)")

        logger.info(
            "[RDV]"
            f" registered {config.peer_id} as"
            f" {response.ip}:{response.port}"
            f" (ttl={response.ttl})"
        )

        return response.ip, response.ttl

    logger.error(f"[RDV] Error at REGISTER: {response.message}")
    raise ValueError(f"{response.message}")


def discover(server: RDVServer, my_id: str, namespace: str | None = None):
    message = RendezvousMessage.build_discover(namespace)
    response = exchange_message(server, message)

    if response.is_ok():
        if not response.peers:
            raise RuntimeError("DISCOVER OK but no 'peers' field")

        peers: list[Peer] = [
            peer
            for peer in [Peer.from_dict(p) for p in response.peers]
            if peer.peer_id != my_id
        ]
        peers_str_list = [str(p) for p in peers]
        peers_str = "\n\t".join(peers_str_list)

        logger.info(f"[RDV] Discovered {len(peers)} peer(s):\n\t{peers_str}")

        return peers

    logger.error(f"[RDV] Error at DISCOVER: {response.message}")
