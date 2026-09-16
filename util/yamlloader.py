import yaml
import os

def load_config(yaml_file:str):
    if not os.path.exists(yaml_file) and os.path.exists(f"{yaml_file}.template"):
        yaml_file = f"{yaml_file}.template"

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
    configured_uri = os.getenv("MONGO_URI")
    if configured_uri:
        return configured_uri

    config = load_config(yaml_file=yaml_file)
    db_pass = os.getenv("MONGO_PASSWORD")
    db_user = os.getenv("MONGO_USERNAME")
    if not db_pass or not db_user:
        raise RuntimeError("MONGO_URI or both MONGO_USERNAME and MONGO_PASSWORD are required")
    return config["db"]["link"].replace("<Password>", db_pass).replace("<User>", db_user)