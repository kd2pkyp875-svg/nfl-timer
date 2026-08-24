import os
import random
import requests
import time
from datetime import datetime

# Paste your actual Discord URL between the quote marks below
WEBHOOK_URL = "https://discord.com/api/webhooks/1539384525753290895/Lb7_JskAPwL-T3X1635SoUnYMoB5Cv0vDknFuXC8MCBm8GgrYn49eGnFpNHD4eeS3JB4"
FILE_NAME = "teams.txt"
ID_FILE = "last_msg.txt"

# Complete master list updated with full city and team names
MASTER_TEAMS = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", 
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", 
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers", 
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs", 
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins", 
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants", 
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers", 
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

def get_season_strings():
    """Automatically calculates '2026/2027' and '26/27' based on current date"""
    current_year = datetime.now().year
    next_year = current_year + 1
    
    full_season = f"{current_year}/{next_year}"
    short_season = f"{str(current_year)[2:]}/{str(next_year)[2:]}"
    return full_season, short_season

def load_teams():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_teams(teams_list):
    with open(FILE_NAME, "w") as f:
        for team in teams_list:
            f.write(f"{team}\n")

def delete_previous_message():
    """Finds and deletes the message sent in the last 10-minute interval"""
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            msg_id = f.read().strip()
        if msg_id:
            delete_url = f"{WEBHOOK_URL}/messages/{msg_id}"
            requests.delete(delete_url)

def save_message_id(response):
    """Saves the unique Discord ID of the newly sent message"""
    if response.status_code == 200:
        try:
            msg_id = response.json().get("id")
            with open(ID_FILE, "w") as f:
                f.write(str(msg_id))
        except Exception:
            pass

def main():
    teams = load_teams()
    
    # If the file happens to be empty at startup, automatically fill it with full names
    if not teams:
        teams = MASTER_TEAMS.copy()
        save_teams(teams)

    # Get the automatic year formatting (e.g., '2026/2027' and '26/27')
    full_season, short_season = get_season_strings()

    while teams:
        selected_team = random.choice(teams)
        teams.remove(selected_team)
        save_teams(teams)
        
        # 1. Delete the previous message from 10 minutes ago
        delete_previous_message()
        
        # 2. Append '?wait=true' to the URL so Discord sends back the message tracking details
        post_url = f"{WEBHOOK_URL}?wait=true"
        
        # CHOOSE THE MESSAGE TYPE:
        if len(teams) == 0:
            # Final winner announcement block
            payload = {
                "embeds": [
                    {
                        "title": f"🏆 {full_season} THIS YEARS ASSIGNED NFL TEAM",
                        "description": f"🎉 **CONGRATS!!! Chan and Kameron for the {short_season} season you are diehard fans for the ||{selected_team}||!!!** 🎉",
"color": 13413120,
"fields": [
    {
        "name": "Your Assigned Franchise",
        "value": f"🏈 **||{selected_team}||**",
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
            requests.post(post_url, json=payload)
            
            # Clear out the ID tracking file since the draft is done
            if os.path.exists(ID_FILE):
                os.remove(ID_FILE)
        else:
            # Elimination format tracking full team names
            # Hidden spacing forces phone alerts to hide the team until clicked
            # Elimination format tracking full team names
            message = f"🏈 Your {short_season} NFL Team is NOT ❌ the: **||{selected_team}||**"


            res = requests.post(post_url, json={"content": message})
            
            # Save the new message ID to use for deletion in the next loop
            save_message_id(res)
        
        if teams:
            time.sleep(600)  # 10 minutes

    # AUTOMATIC RESET: Restore all 32 full teams to the file for the next draft
    save_teams(MASTER_TEAMS)
    requests.post(post_url, json={"content": "🏁 The 32-team loop is done! The team list has automatically reset for your next draft."})

if __name__ == "__main__":
    main()


