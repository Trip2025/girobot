
from main import send_girobot_update, fetch_giro_stage_results
import time
import sys

print("Triggering live GiroBot update for the most recent stage results...")

# Debug mode - if a stage number is provided as argument, try to fetch that specific stage
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    stage_num = int(sys.argv[1])
    print(f"Debug mode: Attempting to fetch Stage {stage_num} results directly...")
    results = fetch_giro_stage_results(stage_num)
    if results:
        print("✅ Successfully fetched stage results:")
        print(f"Winner: {results['stage_winner']} ({results['team']})")
        print(f"Second: {results['second']}")
        print(f"Third: {results['third']}")
        print(f"Time: {results['time']}")
        print(f"Pink Jersey: {results['pink_jersey']}")
        print(f"Points Jersey: {results['points_jersey']}")
        print(f"KOM Jersey: {results['kom_jersey']}")
        print(f"Youth Jersey: {results['youth_jersey']}")
        print("\nContinuing to send WhatsApp message...")
    else:
        print("❌ Could not fetch live results. Falling back to static data.")

print("Sending WhatsApp message with the latest stage results...")
success = send_girobot_update()

if success:
    print("✅ WhatsApp message with the latest stage results sent successfully!")
    print("Check your WhatsApp for the Giro d'Italia update.")
    print("Daily updates will continue automatically until the race concludes on May 25th.")
else:
    print("❌ Failed to send WhatsApp message.")
    print("Check the error messages above for details.")

print("\nNote: For daily automatic updates, ensure the main service is running.")
print("To test specific stages, run: python trigger_live_update.py [stage_number]")
