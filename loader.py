from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import django
from data import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


new_bot = Bot(token=config.BOT_TOKEN_USER, parse_mode=types.ParseMode.HTML)# Замените 'YOUR_NEW_BOT_TOKEN' на токен вашего нового бота
new_storage = MemoryStorage()
new_dp = Dispatcher(new_bot, storage=new_storage)