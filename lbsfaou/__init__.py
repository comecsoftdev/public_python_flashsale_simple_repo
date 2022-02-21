from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


def load_environment():
    # debug .env
    env_file_name = BASE_DIR / '.private' / 'debug' / '.env'
    assert Path.exists(env_file_name), 'ENV_FILE_NAME not exist'
    load_dotenv(dotenv_path=env_file_name, encoding='utf-8')
