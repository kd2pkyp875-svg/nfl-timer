import os
import random
import requests
import time

# Paste your actual Discord URL between the quote marks below
WEBHOOK_URL = "https://discord.com/api/webhooks/1539384525753290895/Lb7_JskAPwL-T3X1635SoUnYMoB5Cv0vDknFuXC8MCBm8GgrYn49eGnFpNHD4eeS3JB4"
FILE_NAME = "teams.txt"

# Complete master list to automatically restore at the end
MASTER_TEAMS = [
    "Cardinals", "Falcons", "Ravens", "Bills", "Panthers", "Bears",
    "Bengals", "Browns", "Cowboys", "Broncos", "Lions", "Packers",
    "Texans", "Colts", "Jaguars", "Chiefs", "Raiders", "Chargers",
    "Rams", "Dolphins", "Vikings", "Patriots", "Saints", "Giants",
    "Jets", "Eagles", "Steelers", "49ers", "Seahawks", "Buccaneers",
    "Titans", "Commanders"
]

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
    
    # If the file happens to be empty at startup, automatically fill it
    if not teams:
        teams = MASTER_TEAMS.copy()
        save_teams(teams)

    # Keep running until all teams in the list are gone
    while teams:
        selected_team = random.choice(teams)
        teams.remove(selected_team)
        
        # Save the shorter list back to the file
        save_teams(teams)
        
        # CHOOSE THE MESSAGE TYPE:
        if len(teams) == 0:
            # High-end structured announcement block layout for Discord
            payload = {
                "embeds": [
                    {
                        "title": "🏆 2026/27 ASSIGNED TEAM",
                        "description": f"🎉 **CONGRATS!!! Chan and Kameron for the 26/27 season you are diehard fans for the {selected_team}!!!** 🎉",
                        "color": 13413120, # Custom Gold Banner Color Code
                        "fields": [
                            {
                                "name": "Your Assigned Franchise",
                                "value": f"🏈 **{selected_team}**",
                                "inline": False
                            },
                            {
                                "name": "Message",
                                "value": "Best of luck on the upcoming season! May you hit the over.",
                                "inline": False
                            }
                        ],
                        "footer": {
                            "text": "NFL Random Selection Loop Completed"
                        }
                    }
                ]
            }
            # Send the special box layout to Discord
            requests.post(WEBHOOK_URL, json=payload)
        else:
            # Standard text message format for all previous teams
            message = f"🏈 Your 26/27 NFL team is NOT: **{selected_team}** ({len(teams)} teams remaining)"
            requests.post(WEBHOOK_URL, json={"content": message})
        
        # If there are still teams left, pause the script for exactly 10 minutes
        if teams:
            time.sleep(600)  # 600 seconds = 10 minutes

    # AUTOMATIC RESET: Restore all 32 teams to the file for the next draft
    save_teams(MASTER_TEAMS)
    requests.post(WEBHOOK_URL, json={"content": "🏁 The 32-team loop is done! The team list has automatically reset for your next draft."})

if __name__ == "__main__":
    main()

