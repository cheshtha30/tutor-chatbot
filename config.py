import yaml
from dotenv import dotenv_values,load_dotenv
from dotenv import load_dotenv


load_dotenv()
# Load YAML file into SETTINGS
with open('settings.yaml', 'r') as file:
    SETTINGS = yaml.safe_load(file)

# Load .env file into SECRETS
SECRETS = dotenv_values(".env")

# Example of how to use SETTINGS and SECRETS in your code
# print(SETTINGS)
# print(SECRETS["OPENAI_APIKEY"])
