
from main import send_girobot_update
import time

print("Triggering live GiroBot update for the most recent stage results...")
print("Sending WhatsApp message with the latest stage results...")

success = send_girobot_update()

if success:
    print("✅ WhatsApp message with Stage 2 results sent successfully!")
    print("Check your WhatsApp for the Giro d'Italia update.")
    print("Daily updates will continue automatically until the race concludes on May 25th.")
else:
    print("❌ Failed to send WhatsApp message.")
    print("Check the error messages above for details.")

print("\nNote: For daily automatic updates, ensure the main service is running.")
