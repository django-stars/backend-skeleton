from pathlib import Path

import environ


env = environ.Env(DEBUG=(bool, False))

current_path = environ.Path(__file__) - 1
site_root = current_path - 2
env_file = site_root(".env")

if Path(env_file).exists():
    environ.Env.read_env(env_file=env_file)
