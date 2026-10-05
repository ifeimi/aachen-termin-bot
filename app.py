import os
import telegram
import asyncio

from dotenv import load_dotenv
from flask import Flask
from flask_apscheduler import APScheduler
from termin import aachen_hbf_termin
from typing import Final
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

load_dotenv()

TOKEN: str = os.getenv("TOKEN", "")

#CHANNEL_ID: Final = '@ifeimitest'
HBF_CHANNEL_ID: Final = '@aachen_aus_termin'

APPOINTMENT_LINK = "https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1"

@app.route('/status')
def status():    
    return 'OK'


@app.route('/')
def hello_world():    
    return 'Hello, World!'


@scheduler.task('interval', id='do_job_1', minutes=20, misfire_grace_time=900)
def job():
    is_available, res = aachen_hbf_termin()
    if is_available:
        text = f"{res}\n[🔥 Book Now\\!]({APPOINTMENT_LINK})"
        text = text.replace(".", "\\.")
        asyncio.run(send_telegram_message(text))


async def send_telegram_message(text: str):
    async with telegram.Bot(token=TOKEN) as bot:
        await bot.send_message(
            chat_id=HBF_CHANNEL_ID,
            text=text,
            parse_mode='MarkdownV2',
        )