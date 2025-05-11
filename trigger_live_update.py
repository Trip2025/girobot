
from main import send_girobot_update
import time

print("Triggering live GiroBot update manually...")
print("Sending WhatsApp message...")

success = send_girobot_update()

if success:
    print("✅ WhatsApp message sent successfully!")
    print("Check your WhatsApp for the Giro d'Italia update.")
else:
    print("❌ Failed to send WhatsApp message.")
    print("Check the error messages above for details.")

print("\nNote: For daily automatic updates, ensure the main service is running.")
