from dotenv import load_dotenv
import yaml

def load_env(path: str):
    if not load_dotenv(path):
        print(f"Failed to load environment variable file at {path}")
        exit(1)

def load_prompts(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file '{file_path}'. Details: {e}")
        exit(1)