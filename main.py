import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "" #Your bot token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await msg.reply("Hi!\n\nI'm bot popocho! \n\nI predict the weather for tomorrow! \n\nTo find out the weather for tomorrow, enter the command /weather")


class City(StatesGroup):
    user_city = State()


@dp.message_handler(commands=["weather"])
async def input_city(msg: types.Message):
    """
    This handler gets city name from user
    """
    await bot.send_message(msg.from_user.id, "Write me the city where you live")
    await City.user_city.set() #Save name city


@dp.message_handler(state=City.user_city)
async def output_weather_to_user(msg: types.Message, state: FSMContext):
    city = msg.text
    appid = "" # Your API token

    response = requests.get("http://api.openweathermap.org/data/2.5/find", 
                        params={"q": city, "type": "like", "units": "metric", "APPID": appid})

    data = response.json()
    city_id = data["list"][0]["id"]

    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                    params={"id": city_id, "units": "metric", "lang": "en", "APPID": appid})
    data = res.json()
    
    await bot.send_message(msg.from_user.id, f"{data['weather'][0]['description']} \nTemperature: {data['main']['temp']}\nMinimum temperature for today: {data['main']['temp_min']} \nMaximum temperature for today: {data['main']['temp_max']}")    
    await state.finish()

#Start
if __name__ == "__main__":
    executor.start_polling(dp)