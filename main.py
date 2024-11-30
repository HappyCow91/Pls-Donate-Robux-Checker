import requests
import time
from colorama import *
import json

### PLS DONATE TOOL PY ###

# THIS TOOL USE ROPROXY AHH

with open('config.json', 'r') as f:
    config_data = json.load(f)

R_COOKIE = config_data.get('Cookie', None)
WEBHOOK = config_data.get('Webhook', None)
COOL = config_data.get('Cooldown', None)
EVERYONE = config_data.get('EveryonePing', None)

def check_pending(cookie, uid):
    res = requests.get(
        url = f"https://economy.roproxy.com/v2/users/{uid}/transaction-totals?timeFrame=Month&transactionType=summary",
        cookies = {
            ".ROBLOSECURITY": cookie
        }
    )

    if res.status_code == 200:
        json = res.json()
        return json["pendingRobuxTotal"]
    else:
        return print(Fore.RED + f"[-] Error for checking pending robux ... {res.text} {res.status_code}")
    
def check_robux(cookie):
    res = requests.get(
        url="https://economy.roproxy.com/v1/user/currency",
        cookies={".ROBLOSECURITY": cookie}
    )

    if res.status_code == 200:
        json = res.json()
        return json["robux"]
    else:
        return print(Fore.RED + f"[-] Error for checking robux ... {res.text} {res.status_code}")
    
def check_easy_info(cookie):
    res = requests.get(
        url="https://users.roproxy.com/v1/users/authenticated",
        cookies={".ROBLOSECURITY": cookie}
    )

    if res.status_code == 200:
        json = res.json()
        return json
    else:
        return "Cookie Invalid !"

def get_thumb(uid):
    res = requests.get(
        url=f"https://thumbnails.roproxy.com/v1/users/avatar-headshot?userIds={uid}&size=420x420&format=Png&isCircular=true"
    )
    if res.status_code == 200:
        json = res.json()
        return json["data"][0]["imageUrl"]

def send_webhook(webhooker, username, display, uid, robux, pending, thumb):
    if EVERYONE == True:
        con = "@everyone"
    else:
        con = None
    
    data = {
        "content": con,
        "embeds": [
            {
                "title": "PENDING NOTIFY",
                "color": 65280,
                "fields": [
                    {
                        "name": "Username",
                        "value": str(username),
                        "inline": True
                    },
                    {
                        "name": "Display",
                        "value": str(display),
                        "inline": True
                    },
                    {
                        "name": "UID",
                        "value": str(uid),
                        "inline": True
                    },
                    {
                        "name": "NOW Robux",
                        "value": str(robux),
                        "inline": True
                    },
                    {
                        "name": "Pending Robux",
                        "value": str(pending),
                        "inline": True
                    },
                ],
                "thumbnail": {
                    "url": thumb
                }
            }
        ]
    }

    try:
        res = requests.post(
            url=webhooker,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )

        if res.status_code == 204:
            print("[+] Webhook sent successfully.")
        else:
            print(f"Error: {res.status_code}, {res.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    print(Fore.GREEN + """
██████╗ ██╗     ███████╗    ███╗   ██╗ ██████╗ ████████╗██╗███████╗██╗   ██╗
██╔══██╗██║     ██╔════╝    ████╗  ██║██╔═══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██████╔╝██║     ███████╗    ██╔██╗ ██║██║   ██║   ██║   ██║█████╗   ╚████╔╝ 
██╔═══╝ ██║     ╚════██║    ██║╚██╗██║██║   ██║   ██║   ██║██╔══╝    ╚██╔╝  
██║     ███████╗███████║    ██║ ╚████║╚██████╔╝   ██║   ██║██║        ██║   
╚═╝     ╚══════╝╚══════╝    ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝╚═╝        ╚═╝   
                                                                            
    """)
    while True:
        ROBUX = check_robux(R_COOKIE)
        info = check_easy_info(R_COOKIE)
        
        if isinstance(info, dict):  # Only proceed if the info is valid
            UID = info["id"]
            PENDING = check_pending(R_COOKIE, UID)
            thumb_url = get_thumb(UID)
            NAME = info["name"]
            DISPLAY = info["displayName"]

            # SENDER
            send_webhook(WEBHOOK, NAME, DISPLAY, UID, ROBUX, PENDING, thumb_url)
        else:
            print(Fore.RED + "Invalid Cookie. Please try again.")
            break

        # Wait for config time
        time.sleep(COOL)

if __name__ == "__main__":
    main()
