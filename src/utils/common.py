import yaml
import os
from box import ConfigBox




def read_yaml(path_to_yaml: str) -> ConfigBox:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return ConfigBox(content)



def create_directories(path_to_directories):
        os.makedirs(path_to_directories, exist_ok=True)