from environs import Env

env = Env()
env.read_env()
TOKEN = env('BOT_TOKEN')
FREE_LINK_LIMIT= int(env('FREE_LINK_LIMIT'))