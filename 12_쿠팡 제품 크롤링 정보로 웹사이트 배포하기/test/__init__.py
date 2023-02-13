from pathlib import Path
import sys
import os

BASE_DIR : str = os.path.dirname(Path(__file__).resolve().parent)
sys.path.append(BASE_DIR)
from html_maker import create_dir , html_maker , get_env , sftp_to_gcp
from src.main import Coupang