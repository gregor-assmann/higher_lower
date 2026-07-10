import yaml
import os

def load_config(yaml_file:str):
    try:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)

        if data:
            return data
        else:
            print("Config", "No 'categories' in config-file")

    except FileNotFoundError:
        print("File", f"File '{yaml_file}' not found.")
    except yaml.YAMLError as e:
        print("Yaml", f"Failed parsing Yaml File", e)

def load_db_uri(yaml_file: str) -> str:
    config = load_config(yaml_file="game_config.yaml")
    db_pass = os.getenv("MONGO_PASSWORD")
    db_user = os.getenv("MONGO_USERNAME")
    return config["db"]["link"].replace("<Password>", db_pass).replace("<User>", db_user)