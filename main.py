from flask import Flask
from threading import Thread
import time
from datetime import datetime, timedelta
import pytz
from twilio.rest import Client
import os

app = Flask(__name__)

# Load secrets from environment variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_whatsapp_number = os.environ['TWILIO_FROM_NUMBER']
to_whatsapp_number = os.environ['TO_NUMBER']

client = Client(account_sid, auth_token)

def send_girobot_update():
    message = client.messages.create(
        body=(
            "🚴‍♂️ *GiroBot Daily Update – Sunday 11 May*\n\n"
            "🏁 *Stage 2 Summary*\n"
            "🏆 Winner: Juan Ayuso (UAE Team Emirates)\n"
            "🥈 2nd: Wout van Aert\n"
            "🥉 3rd: Jonathan Milan\n"
            "⏱️ Time: 4h 16m 21s\n\n"
            "🟣 *Lidl–Trek Highlights*\n"
            "✅ Pedersen finished 6th in sprint finish\n"
            "📊 Team standing: 2nd in Team Classification\n"
            "😎 All riders finished safely\n\n"
            "🎽 *Jersey Leaders*\n"
            "🩷 Maglia Rosa: Juan Ayuso\n"
            "🟣 Points: Mads Pedersen\n"
            "🔵 KOM: Einer Rubio\n"
            "⚪ Youth: Juan Ayuso\n\n"
            "📰 *Top Story*: Ayuso attacks late, takes Pink and White\n"
            "🔗 Read more: https://www.cyclingnews.com/races/giro-d-italia-2025/\n\n"
            "🕗 Next update: 8:00 AM AEST tomorrow."
        ),
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    print(f"Sent message SID: {message.sid}")

def scheduler():
    aest = pytz.timezone("Australia/Melbourne")
    while True:
        now = datetime.now(aest)
        target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        wait_time = (target_time - now).total_seconds()
        print(f"Sleeping for {wait_time / 60:.2f} minutes until next send...")
        time.sleep(wait_time)
        send_girobot_update()

@app.route('/')
def home():
    return "GiroBot Flask App Running"

@app.route('/trigger')
def manual_trigger():
    send_girobot_update()
    return "Manual GiroBot update sent."

# Start the background scheduler
Thread(target=scheduler, daemon=True).start()

if __name__ == '__main__':
    print("Triggering GiroBot update manually from main.py...")
    send_girobot_update()
    app.run(host='0.0.0.0', port=3000)
