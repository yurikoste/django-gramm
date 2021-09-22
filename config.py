from os import getenv
from pathlib import Path
from dotenv import load_dotenv


class Config(object):

    # General Config
    load_dotenv(Path(__file__).parent / '.env')

