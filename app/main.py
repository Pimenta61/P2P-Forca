from config_loader import load_config, Config

def main():
    cfg: Config = load_config()
    print(cfg.peer_id)

if __name__ == "__main__":
    main()
