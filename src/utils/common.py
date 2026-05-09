import yaml
import os
from box import ConfigBox
import pickle




def read_yaml(path_to_yaml: str) -> ConfigBox:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return ConfigBox(content)



def create_directorie(path_to_directorie):
        os.makedirs(path_to_directorie, exist_ok=True)



def save_model(model,model_path):
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)



def load_model(model_path):
     with open(model_path, 'rb') as file:
        load_model = pickle.load(file)
        return load_model