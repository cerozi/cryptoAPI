from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .crypto_model_update import update_crypto

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_crypto, 'interval', minutes=15)
    scheduler.start()