import environ

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(".env")
