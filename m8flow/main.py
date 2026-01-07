# m8flow/main.py

from dotenv import load_dotenv
load_dotenv()

from m8flow.env import apply_env_mapping
apply_env_mapping()

from m8flow.db.migrate import upgrade_if_enabled
upgrade_if_enabled()  # <-- runs M8Flow migrations

from spiff_web_server import connexion_app
app = connexion_app






# from dotenv import load_dotenv
# load_dotenv()  # 👈 loads .env into os.environ

# from m8flow.env import apply_env_mapping
# apply_env_mapping()

# from spiff_web_server import connexion_app

# app = connexion_app

