import yaml

def load_yaml_config(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)