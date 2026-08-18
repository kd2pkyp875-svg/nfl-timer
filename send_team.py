import os
import random
import requests

# Paste your actual Discord URL between the quote marks below
WEBHOOK_URL = "https://discord.com/api/webhooks/1539384525753290895/Lb7_JskAPwL-T3X1635SoUnYMoB5Cv0vDknFuXC8MCBm8GgrYn49eGnFpNHD4eeS3JB4"

FILE_NAME = "teams.txt"

def send_random_team():
    # Check if the file exists
    if not os.path.exists(FILE_NAME):
        requests.post(WEBHOOK_URL, json={"content": "🚨 Error: teams.txt file is missing!"})
        return

    # Read all remaining teams
    with open(FILE_NAME, "r") as f:
        teams = [line.strip() for line in f.readlines() if line.strip()]

    # Check if we ran out of teams
    if not teams:
        requests.post(WEBHOOK_URL, json={"content": "🏈 All 32 NFL teams have been sent! The list is now empty."})
        return

    # Pick a random team and remove it from the list
    selected_team = random.choice(teams)
    teams.remove(selected_team)

    # Save the remaining teams back to the file
    with open(FILE_NAME, "w") as f:
        for team in teams:
            f.write(f"{team}\n")

    # Send the message to Discord
    message = f"🏈 Your random NFL team is: **{selected_team}** ({len(teams)} teams remaining)"
    requests.post(WEBHOOK_URL, json={"content": message})

if __name__ == "__main__":
    send_random_team()
