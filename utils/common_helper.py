import yaml


def read_config(config):
    with open(config) as config:
        content = yaml.safe_load(config)

    return content
