import logging

from app import rendezvous_client
from app.config_loader import Config, load_config


def setup_logging(log_file: str | None = None):
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(fmt))

    handlers: list = [console_handler]

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(fmt))
        handlers.append(file_handler)

    logging.basicConfig(level=logging.DEBUG, handlers=handlers)


def main():
    cfg: Config = load_config()
    setup_logging(cfg.log_file)
    rendezvous_client.register(cfg)


if __name__ == "__main__":
    main()
