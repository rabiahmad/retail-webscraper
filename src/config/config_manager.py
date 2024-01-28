import yaml


def combine_configs(*args):
    config = {}
    for entry in args:
        config[entry[0]] = get_config(entry[1])
    return config


def get_config(yaml_file_path):
    with open(yaml_file_path, "rt") as f:
        config = yaml.safe_load(f.read())
    return config


config_entries = (
    ["logging", "src/config/logging_config.yaml"],
    ["settings", "src/config/settings.yaml"],
)

config = combine_configs(*config_entries)
