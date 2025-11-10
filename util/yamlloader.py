import yaml

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

