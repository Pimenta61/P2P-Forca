import json
import logging
import socket

from app.config_loader import Config
from app.messages import RendezvousMessage

logger = logging.getLogger(__name__)

MAX_MESSAGE_LEN_BYTES = 32 * 1024  # 32 KB


def send_register(server: tuple, message: RendezvousMessage):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server)

        message_encoded = message.to_json().encode()

        sock.sendall(message_encoded)
        logger.debug(f"Sent REGISTER:\n {message.to_json()}")

        response_bytes = sock.recv(MAX_MESSAGE_LEN_BYTES)
        if not response_bytes:
            raise RuntimeError("Empty response from Rendezvous server")

        response_dict = json.loads(response_bytes.decode("utf-8"))
        return RendezvousMessage.from_dict(response_dict)


def register(config: Config) -> tuple[str, int] | None:
    server = (config.rdv_host, config.rdv_port)
    message = RendezvousMessage.build_register(config)
    response = send_register(server, message)

    logger.debug(f"Received :\n {response.to_json()}")

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

    logger.error(f"Error at REGISTER: {response.message}")
    raise ValueError(f"{response.message}")
