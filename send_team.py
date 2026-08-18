import os
import random
import requests
import time

# Paste your actual Discord URL between the quote marks below
WEBHOOK_URL = "https://discord.com/api/webhooks/1539384525753290895/Lb7_JskAPwL-T3X1635SoUnYMoB5Cv0vDknFuXC8MCBm8GgrYn49eGnFpNHD4eeS3JB4"
FILE_NAME = "teams.txt"

def load_teams():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_teams(teams_list):
    with open(FILE_NAME, "w") as f:
        for team in teams_list:
            f.write(f"{team}\n")

def main():
    teams = load_teams()
    
    if not teams:
        requests.post(WEBHOOK_URL, json={"content": "🏈 The team list is already empty!"})
        return

    # Keep running until all teams in the list are gone
    while teams:
        selected_team = random.choice(teams)
        teams.remove(selected_team)
        
        # Instantly save the shorter list back to the file
        save_teams(teams)
        
        # Send the message to Discord
        message = f"🏈 Your 26/27 NFL team is NOT: **{selected_team}** ({len(teams)} teams remaining)"
        requests.post(WEBHOOK_URL, json={"content": message})
        
        # If there are still teams left, pause the script for exactly 10 minutes
        if teams:
            time.sleep(600)  # 600 seconds = 10 minutes

    requests.post(WEBHOOK_URL, json={"content": "🎉 All 32 NFL teams have been sent!"})

if __name__ == "__main__":
    main()
