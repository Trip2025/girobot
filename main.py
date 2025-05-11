
from flask import Flask
from threading import Thread
import time
from datetime import datetime, timedelta
import pytz
from twilio.rest import Client
import os
import requests
import json

app = Flask(__name__)

# Load secrets from environment variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_whatsapp_number = os.environ['TWILIO_FROM_NUMBER']
to_whatsapp_number = os.environ['TO_NUMBER']

client = Client(account_sid, auth_token)

def get_giro_update():
    """
    In a real app, this would fetch real-time data from an API.
    For now, we'll use static demo data with the current date.
    """
    today = datetime.now(pytz.timezone("Australia/Melbourne"))
    date_str = today.strftime("%A %d %B")
    
    # Demo data - in a real app, this would come from an API
    return {
        "date": date_str,
        "stage_num": "9",
        "stage_winner": "Tadej Pogačar",
        "team": "UAE Team Emirates",
        "second": "Geraint Thomas",
        "third": "Daniel Martinez",
        "time": "4h 48m 33s",
        "lidl_trek_highlight": "Giulio Ciccone finished 7th on the mountain stage",
        "team_standing": "3rd in Team Classification",
        "team_safety": "All riders finished safely",
        "pink_jersey": "Tadej Pogačar",
        "points_jersey": "Jonathan Milan",
        "kom_jersey": "Giulio Ciccone",
        "youth_jersey": "Tadej Pogačar",
        "top_story": "Pogačar extends lead with dominant mountain performance",
        "link": "https://www.cyclingnews.com/races/giro-d-italia-2025/"
    }

def format_giro_message(data):
    """Format the Giro update into a WhatsApp message"""
    message = (
        f"🚴‍♂️ *GiroBot Daily Update – {data['date']}*\n\n"
        f"🏁 *Stage {data['stage_num']} Summary*\n"
        f"🏆 Winner: {data['stage_winner']} ({data['team']})\n"
        f"🥈 2nd: {data['second']}\n"
        f"🥉 3rd: {data['third']}\n"
        f"⏱️ Time: {data['time']}\n\n"
        f"🟣 *Lidl–Trek Highlights*\n"
        f"✅ {data['lidl_trek_highlight']}\n"
        f"📊 Team standing: {data['team_standing']}\n"
        f"😎 {data['team_safety']}\n\n"
        f"🎽 *Jersey Leaders*\n"
        f"🩷 Maglia Rosa: {data['pink_jersey']}\n"
        f"🟣 Points: {data['points_jersey']}\n"
        f"🔵 KOM: {data['kom_jersey']}\n"
        f"⚪ Youth: {data['youth_jersey']}\n\n"
        f"📰 *Top Story*: {data['top_story']}\n"
        f"🔗 Read more: {data['link']}\n\n"
        f"🕗 Next update: 8:00 AM AEST tomorrow."
    )
    return message

def send_girobot_update():
    """Send the Giro update via WhatsApp"""
    try:
        data = get_giro_update()
        message_body = format_giro_message(data)
        
        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )
        print(f"WhatsApp message sent successfully! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        return False

def scheduler():
    """Schedule daily updates at 8am AEST"""
    aest = pytz.timezone("Australia/Melbourne")
    print(f"GiroBot scheduler started. Will send updates daily at 8:00 AM AEST.")
    
    while True:
        now = datetime.now(aest)
        target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
        
        # If it's already past 8am, schedule for tomorrow
        if now > target_time:
            target_time += timedelta(days=1)
            
        wait_seconds = (target_time - now).total_seconds()
        next_run = now + timedelta(seconds=wait_seconds)
        
        print(f"Next update scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Sleeping for {wait_seconds / 60:.1f} minutes until next send...")
        
        time.sleep(wait_seconds)
        send_girobot_update()

@app.route('/')
def home():
    next_update = get_next_update_time()
    return f"""
    <html>
        <head>
            <title>GiroBot WhatsApp Service</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #e91e63; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .info {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
                .footer {{ margin-top: 40px; font-size: 0.8em; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚴‍♂️ GiroBot WhatsApp Service</h1>
                <div class="info">
                    <p><strong>Status:</strong> Running</p>
                    <p><strong>Next scheduled update:</strong> {next_update}</p>
                    <p>This service sends daily Giro d'Italia updates via WhatsApp at 8:00 AM AEST.</p>
                </div>
                <p>Use the following endpoints:</p>
                <ul>
                    <li><a href="/trigger">/trigger</a> - Send a test update immediately</li>
                    <li><a href="/health">/health</a> - Check service health</li>
                </ul>
                <div class="footer">
                    <p>GiroBot Service · Running on Replit</p>
                </div>
            </div>
        </body>
    </html>
    """

def get_next_update_time():
    """Get the next scheduled update time string"""
    aest = pytz.timezone("Australia/Melbourne")
    now = datetime.now(aest)
    target = now.replace(hour=8, minute=0, second=0, microsecond=0)
    if now > target:
        target += timedelta(days=1)
    return target.strftime("%Y-%m-%d %H:%M:%S %Z")

@app.route('/trigger')
def manual_trigger():
    """Endpoint to manually trigger an update"""
    if send_girobot_update():
        return """
        <html>
            <head>
                <title>GiroBot Manual Trigger</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .success { color: green; }
                </style>
            </head>
            <body>
                <h2 class="success">✅ Manual GiroBot update sent successfully!</h2>
                <p>Check your WhatsApp for the message.</p>
                <p><a href="/">Back to home</a></p>
            </body>
        </html>
        """
    else:
        return """
        <html>
            <head>
                <title>GiroBot Manual Trigger</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .error { color: red; }
                </style>
            </head>
            <body>
                <h2 class="error">❌ Error sending update</h2>
                <p>Check the console logs for details.</p>
                <p><a href="/">Back to home</a></p>
            </body>
        </html>
        """

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "next_update": get_next_update_time()}

# Start the background scheduler
scheduler_thread = Thread(target=scheduler, daemon=True)

if __name__ == '__main__':
    print("Starting GiroBot WhatsApp service...")
    scheduler_thread.start()
    print("Sending initial test message...")
    send_girobot_update()
    app.run(host='0.0.0.0', port=3000)
else:
    # This ensures the scheduler runs when deployed with Gunicorn or similar
    scheduler_thread.start()
