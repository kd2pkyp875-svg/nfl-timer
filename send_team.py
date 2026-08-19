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
        
        # CHOOSE THE MESSAGE TYPE:
        # If this is the absolute last team (0 remaining in the list), send the custom congrats message!
        if len(teams) == 0:
            message = f"🎉 **CONGRATS!!! Chan and Kameron for the 26/27 season you are diehard fans for the {selected_team}!!! Best of luck on the season!!!** 🎉"
        else:
            # Standard message for all previous teams
            message = f"🏈 Your 26/27 NFL team is NOT: **{selected_team}** ({len(teams)} teams remaining)"
        
        # Send the message to Discord
        requests.post(WEBHOOK_URL, json={"content": message})
        
        # If there are still teams left, pause the script for exactly 10 minutes
        if teams:
            time.sleep(600)  # 600 seconds = 10 minutes

    # Optional final confirmation message once the loop fully exits
    requests.post(WEBHOOK_URL, json={"content": "🏁 The 32-team selection loop has finished successfully."})

if __name__ == "__main__":
    main()
