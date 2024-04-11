from typing import Final
import requests
import telegram
from dotenv import load_dotenv
import os
from flask import Flask
from flask_apscheduler import APScheduler
from termin import aachen_termin
from utils import get_next_months

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

load_dotenv()

TOKEN = os.getenv("TOKEN")
# BOT_USERNAME: Final = '@aachen_termin_bot'
CHANNEL_ID: Final = '@aachen_aus_termin'
#URL: Final = 'https://aachen-termin-bot.onrender.com'

# https://serviceportal.aachen.de/suche/-/vr-bis-detail/dienstleistung/5790/show


@app.route('/status')
def status():    
    return 'OK'

@app.route('/')
def hello_world():    
    return 'Hello, World!'

@scheduler.task('interval', id='do_job_1', seconds=300, misfire_grace_time=900)
def job1():    
    bot = telegram.Bot(token=TOKEN)
    notify_aachen_termin(bot)
    

def notify_aachen_termin(bot: telegram.Bot):
    is_available, res = aachen_termin()
    if is_available:
        bot.send_message(chat_id=CHANNEL_ID, text=res)  


#@scheduler.task('interval', id='do_job_2', seconds=300, misfire_grace_time=900)
#def job2():
    #r = requests.get(f'{URL}/status')
    #print(r)