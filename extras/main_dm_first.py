import requests
import json
from colorama import Fore, Style
from pystyle import Write, System, Colors, Colorate, Anime
from datetime import datetime
import getpass
import random
import os
import threading

TOKEN = '' # For single advertising
DEBUG = False # If the messages somehow does not send, set this to true to see more detailed errors and more informations
DETAILED = True # Leave it on True if you want to use it as a tool, It will just print in the console success/failed/captcha tokens

if TOKEN == '' or None:
   with open('tokens.txt', 'r') as f:
    TOKEN = [line.strip() for line in f.readlines()]
else:
    TOKEN = TOKEN

class logger:
    def __init__(self, prefix: str = ".gg/bestnitro"):
        self.WHITE: str = "\u001b[37m"
        self.MAGENTA: str = "\033[38;5;97m"
        self.MAGENTAA: str = "\033[38;2;157;38;255m"
        self.RED: str = "\033[38;5;196m"
        self.GREEN: str = "\033[38;5;40m"
        self.YELLOW: str = "\033[38;5;220m"
        self.BLUE: str = "\033[38;5;21m"
        self.PINK: str = "\033[38;5;176m"
        self.CYAN: str = "\033[96m"
        self.prefix: str = f"{self.PINK}[{self.MAGENTA}{prefix}{self.PINK}] "

    def message3(self, level: str, message: str, start: int = None, end: int = None) -> str:
        time = self.get_time()
        return f"{self.prefix}[{self.MAGENTAA}{time}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {self.CYAN}{message}{Fore.RESET}"

    def get_time(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def success(self, message: str, start: int = None, end: int = None, level: str = "Success") -> None:
        print(self.message3(f"{self.GREEN}{level}", f"{self.GREEN}{message}", start, end))

    def failure(self, message: str, start: int = None, end: int = None, level: str = "Failure") -> None:
        print(self.message3(f"{self.RED}{level}", f"{self.RED}{message}", start, end))

    def message(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        if start is not None and end is not None:
            print(f"{self.prefix}[{self.MAGENTAA}{time}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET} [{Fore.CYAN}{end - start}s{Style.RESET_ALL}]")
        else:
            print(f"{self.prefix}[{self.MAGENTAA}{time}] {self.PINK}[{Fore.BLUE}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")

    def question(self, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        i = input(f"{self.prefix}[{self.MAGENTAA}{time}] {Fore.RESET} {self.PINK}[{Fore.BLUE}?{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")
        return i

    def info(self, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        print(f"{self.prefix}[{self.MAGENTAA}{time}] {Fore.RESET} {self.PINK}[{Fore.BLUE}!{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")

def truncate_token(token, max_length=10):
    if len(token) > max_length:
        return token[:max_length] + '...'
    else:
        return token

username = getpass.getuser()

def home():
    os.system('cls' if os.name == 'nt' else 'clear')
    Write.Print(f"""

    \t\t  /$$      /$$                                     /$$$$$$        /$$                                 /$$     /$$                              
    \t\t | $$$    /$$$                                    /$$__  $$      | $$                                | $$    |__/                              
    \t\t | $$$$  /$$$$  /$$$$$$   /$$$$$$$ /$$$$$$$      | $$  \ $$  /$$$$$$$ /$$    /$$ /$$$$$$   /$$$$$$  /$$$$$$   /$$  /$$$$$$$  /$$$$$$   /$$$$$$ 
    \t\t | $$ $$/$$ $$ |____  $$ /$$_____//$$_____/      | $$$$$$$$ /$$__  $$|  $$  /$$//$$__  $$ /$$__  $$|_  $$_/  | $$ /$$_____/ /$$__  $$ /$$__  $$
    \t\t | $$  $$$| $$  /$$$$$$$|  $$$$$$|  $$$$$$       | $$__  $$| $$  | $$  \  $$$/ | $$$$$$$$| $$  \__/  | $$    | $$|  $$$$$$ | $$$$$$$$| $$  \__/
    \t\t | $$\  $ | $$ /$$__  $$ \____  $$\____  $$      | $$  | $$| $$  | $$   \  $/  | $$_____/| $$        | $$ /$$| $$ \____  $$| $$_____/| $$      
    \t\t | $$ \/  | $$|  $$$$$$$ /$$$$$$$//$$$$$$$/      | $$  | $$|  $$$$$$$    \_/    \_______/| $$        |  $$$$/| $$ /$$$$$$$/|  $$$$$$$| $$      
    \t\t |__/     |__/ \_______/|_______/|_______/       |__/  |__/ \_______/     \_/     \_______/|__/         \___/  |__/|_______/  \_______/|__/      
    \t\t             
    \t\t                                      Welcome {username} | discord.gg/bestnitro  
    \t\t                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    \t\t  ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n""", Colors.red_to_blue, interval=0.0000)

log = logger()
home()
# Read proxies from file
with open('proxies.txt', 'r') as f:
    proxies = [line.strip() for line in f.readlines()]

# Ask user for message
message = log.question(f"Enter the message you want to send: ")
try:
    threads_count = int(log.question(f"Enter the number of threads to use: "))
except Exception:
    threads_count = 10 # Base Threads

home()
# Send message to all available DMs and channels
def send_message(token, used_tokens):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    # Choose a random proxy
    proxy = random.choice(proxies)
    proxies_dict = {
        'http': "http://" + proxy,
        'https': "http://" + proxy
    }

    try:
        # Get the user's DMs
        response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers, proxies=proxies_dict)
        if response.status_code == 401:
            log.failure(f"Invalid token: {truncate_token(token)}")
            with open('invalid.txt', 'a') as f:
                f.write(token + '\n')

            # Remove the token from the TOKEN list
            TOKEN.remove(token)

            # Save the updated TOKEN list to the tokens.txt file
            with open('tokens.txt', 'w') as f:
                for token in TOKEN:
                    f.write(token + '\n')
            return
        elif response.status_code == 429:
            log.failure(f"Rate limited for token: {truncate_token(token)} {response.text}")
        elif response.status_code != 200 and DEBUG:
            log.failure(f"Failed to get DMs for token {truncate_token(token)}: {response.status_code} - {response.text}")
        else:
            dms = json.loads(response.text)
            for dm in dms:
                # Check if the DM is with a bot
                if dm['recipients'][0]['bot']:
                    continue

                # Check if token has already been used to send a message to this DM
                if dm["id"] in used_tokens:
                    continue

                req1 = requests.post(f'https://discord.com/api/v9/channels/{dm["id"]}/messages', headers=headers, json={'content': message}, proxies=proxies_dict)
                if req1.status_code == 200 and DETAILED:
                    log.message("Success", f"Successfully sent message to DM {dm['name']} {truncate_token(token)}")
                elif req1.status_code == 401:
                    log.failure(f"Invalid token: {truncate_token(token)}")
                    with open('invalid.txt', 'a') as f:
                        f.write(token + '\n')

                    # Remove the token from the TOKEN list
                    TOKEN.remove(token)

                    # Save the updated TOKEN list to the tokens.txt file
                    with open('tokens.txt', 'w') as f:
                        for token in TOKEN:
                            f.write(token + '\n')
                    return
                elif req1.status_code == 429:
                    log.failure(f"Rate limited for token: {truncate_token(token)} {req1.text}")
                elif req1.status_code == 403 and "captcha" in req1.text and DETAILED:
                    log.failure(f"Captcha required for token: {truncate_token(token)}")
                elif req1.status_code == 403:
                    log.failure(f"Missing access/perms for token: {truncate_token(token)} in DM {dm['name']}")
                elif req1.status_code != 200 and DEBUG:
                    log.failure(f"Failed to send message to DM {dm['name']} - {dm['id']} for token {truncate_token(token)}: {req1.status_code} - {req1.text}")

                # Mark token as used for this DM
                used_tokens.add(dm["id"])

        # Get the user's guilds
        response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers, proxies=proxies_dict)
        if response.status_code == 401:
            log.failure(f"Invalid token: {truncate_token(token)}")
            with open('invalid.txt', 'a') as f:
                f.write(token + '\n')

            # Remove the token from the TOKEN list
            TOKEN.remove(token)

            # Save the updated TOKEN list to the tokens.txt file
            with open('tokens.txt', 'w') as f:
                for token in TOKEN:
                    f.write(token + '\n')
            return
        elif response.status_code == 429:
            log.failure(f"Rate limited for token: {truncate_token(token)} {response.text}")
        elif response.status_code != 200 and DEBUG:
            log.failure(f"Failed to get guilds for token {truncate_token(token)}: {response.status_code} - {response.text}")

        guilds = json.loads(response.text)

        # Send message to all available channels
        for guild in guilds:
            response = requests.get(f'https://discord.com/api/v9/guilds/{guild["id"]}/channels', headers=headers, proxies=proxies_dict)
            if response.status_code != 200 and DEBUG:
                log.failure(f"Failed to get channels for guild {guild['name']} - {guild['id']} for token {truncate_token(token)}: {response.status_code} - {response.text}")
                continue

            channels = json.loads(response.text)
            if DEBUG:
                log.info(f"Got guild {guild['name']} - {guild['id']}")
            for channel in channels:
                if DEBUG:
                    log.info(f"Got channel {channel['name']} - {channel['id']} in {guild['name']} - {guild['id']}")
                if channel['type'] == 0:  # Text channel
                    # Check if token has already been used to send a message to this channel
                    if (channel["id"], guild["id"]) in used_tokens:
                        continue
                    req1 = requests.post(f'https://discord.com/api/v9/channels/{channel["id"]}/messages', headers=headers, json={'content': message}, proxies=proxies_dict)
                    if req1.status_code == 200 and DETAILED:
                        log.message("Success", f"Successfully sent message to {channel['name']} in {guild['name']} {truncate_token(token)}")
                    elif req1.status_code == 401:
                        log.failure(f"Invalid token: {truncate_token(token)}")
                        with open('invalid.txt', 'a') as f:
                            f.write(token + '\n')

                        # Remove the token from the TOKEN list
                        TOKEN.remove(token)

                        # Save the updated TOKEN list to the tokens.txt file
                        with open('tokens.txt', 'w') as f:
                            for token in TOKEN:
                                f.write(token + '\n')
                        return
                    elif req1.status_code == 429:
                        log.failure(f"Rate limited for token: {truncate_token(token)} {req1.text}")

                    elif req1.status_code == 403 and "captcha" in req1.text and DETAILED:
                        log.failure(f"Captcha required for token: {truncate_token(token)}")

                    elif req1.status_code == 403:
                        log.failure(f"Missing access/perms for token: {truncate_token(token)} in channel {channel['name']} in server {guild['name']}")

                    elif req1.status_code != 200 and DEBUG:
                        log.failure(f"Failed to send message to channel {channel['name']} - {channel['id']} in guild {guild['name']} - {guild['id']} for token {truncate_token(token)}: {req1.status_code} - {req1.text}")

                    # Mark token as used for this channel
                    used_tokens.add((channel["id"], guild["id"]))

    except Exception as e:
        if DEBUG:
            print(e)
        else:
            pass

used_tokens = set()

# Send message indefinitely
threads_pool = []
for token in TOKEN:
    for _ in range(threads_count):
        t = threading.Thread(target=send_message, args=(token, used_tokens))
        threads_pool.append(t)

for t in threads_pool:
    t.start()

# Wait for all threads to finish
for t in threads_pool:
    t.join()
