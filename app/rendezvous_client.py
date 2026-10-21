import json, logging
from app.config_loader import Config
import socket

from app.messages import RendezvousMessage

logger = logging.getLogger(__name__)

MAX_MESSAGE_LEN_BYTES = 32 * 1024 # 32 KB

def register(config: Config) -> RendezvousMessage:
    server = (config.rdv_host, config.rdv_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server)
        
        message = RendezvousMessage.build_register(config)
        message_encoded = message.to_json().encode()

        sock.sendall(message_encoded)
        logger.debug(f"Sent REGISTER:\n {message.to_json()}")

        response_bytes = sock.recv(MAX_MESSAGE_LEN_BYTES)
        if not response_bytes:
            raise RuntimeError("Empty response from Rendezvous server")
        
        response_dict = json.loads(response_bytes.decode("utf-8"))
        response = RendezvousMessage.from_dict(response_dict)

        logger.info("[RDV]"
                f" registered {config.peer_id} as"
                f" {response.ip}:{response.port}"
                f" (ttl={response.ttl})"
                )
        logger.debug(f"Received :\n {response.to_json()}")

        return response
        
