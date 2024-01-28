import yaml


def combine_configs():
    config = {}

    # Add more configs here as necessary
    logging_config = get_config("src/config/logging_config.yaml")
    config["logging"] = logging_config

    return config


def get_config(yaml_file_path):
    with open(yaml_file_path, "rt") as f:
        config = yaml.safe_load(f.read())
    return config


config = combine_configs()
