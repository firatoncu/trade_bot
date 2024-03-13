import yaml

def configs(value):
    # Reading YAML data
    with open("src/config.yaml", 'r') as f:
        confs = yaml.load(f, Loader=yaml.SafeLoader)

    return confs[value]