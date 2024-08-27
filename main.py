import requests
import json
from colorama import Fore, Style
from pystyle import Write, System, Colors, Colorate, Anime
from datetime import datetime
import getpass
import random
import os
from concurrent.futures import ThreadPoolExecutor
import webbrowser
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep


TOKEN = ''  # For single advertising
DEBUG = False  # If the messages somehow do not send, set this to true to see more detailed errors and more informations
DETAILED = True  # Leave it on True if you want to use it as a tool, It will just print in the console success/failed/captcha tokens
PROXY_CHECKER = True # Leave it on True, it will check all of your proxies for errors and remove them if there are some.

if TOKEN == '' or None:
    with open('tokens.txt', 'r') as f:
        TOKEN = [line.strip() for line in f.readlines()]
else:
    TOKEN = TOKEN

class Logger:
    def __init__(self, prefix: str = ".gg/bestnitro"):
        self.WHITE = "\u001b[37m"
        self.MAGENTA = "\033[38;5;97m"
        self.MAGENTAA = "\033[38;2;157;38;255m"
        self.RED = "\033[38;5;196m"
        self.GREEN = "\033[38;5;40m"
        self.YELLOW = "\033[38;5;220m"
        self.BLUE = "\033[38;5;21m"
        self.PINK = "\033[38;5;176m"
        self.CYAN = "\033[96m"
        self.prefix = f"{self.PINK}[{self.MAGENTA}{prefix}{self.PINK}] "

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
    
    def message2(self, level: str, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        if start is not None and end is not None:
            print(f"{self.prefix}[{self.MAGENTAA}{time}] {self.PINK}[{self.CYAN}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET} [{Fore.CYAN}{end - start}s{Style.RESET_ALL}]", end="\r")
        else:
            print(f"{self.prefix}[{self.MAGENTAA}{time}] {self.PINK}[{Fore.BLUE}{level}{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}", end="\r")

    def question(self, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        i = input(f"{self.prefix}[{self.MAGENTAA}{time}] {Fore.RESET} {self.PINK}[{Fore.BLUE}?{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")
        return i

    def info(self, message: str, start: int = None, end: int = None) -> None:
        time = self.get_time()
        print(f"{self.prefix}[{self.MAGENTAA}{time}] {Fore.RESET} {self.PINK}[{Fore.BLUE}!{self.PINK}] -> {Fore.RESET} {self.CYAN}{message}{Fore.RESET}")

class Loader:
    def __init__(self, desc="Loading...", end="\r", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.time = datetime.now().strftime("%H:%M:%S")

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self
    log = Logger()
    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{log.PINK}[{log.MAGENTA}.gg/bestnitro{log.PINK}] {log.MAGENTAA}{self.time}] {log.PINK}[{Fore.BLUE}Checker{log.PINK}] -> {Fore.RESET} {log.GREEN}{self.desc}{Fore.RESET} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()
    

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()

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
    \t\t                                      Welcome {username} | discord.cyberious.xyz  
    \t\t                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    \t\t  ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════\n""", Colors.red_to_blue, interval=0.0000)

log = Logger()
home()
# Read proxies from file
with open('proxies.txt', 'r') as f:
    proxies = [line.strip() for line in f.readlines()]

if not proxies:
    seconds = 5
    log.message("Error", f"No proxies found in proxies.txt")

    while seconds > -1:
        sleep(1)
        log.message2("Info", f"Redirecting to the proxy provider website in {seconds} seconds")
        seconds -= 1
        

    webbrowser.open_new_tab("https://nitroseller0.mysellix.io/fr/product/sticky-residential-proxies-0-3-gb")
    input(Fore.BLUE + "Press any key to exit..." + Fore.RESET)
    exit()

# ------------------------------ SCRIPT BELOW WORKING BUT UNDER CONSTRUCTION ------------------------------ #
checking = False

def test_proxy(proxy):
    try:
        response = requests.get('https://httpbin.org/ip', proxies={'http': "http://" + proxy, 'https': "http://" + proxy}, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        if DEBUG:
            log.failure(f'Error {e} for proxy: {proxy}')
        return False

def exit_message():  
    input(Fore.BLUE + "Press any key to exit..." + Fore.RESET)
    exit()

def check_proxies(proxies):
    format_issues = []
    http_issues = []
    valid_proxies = []
    
    with Loader(f"Checking Proxies..."):
        for proxy in proxies:
            if not proxy.split("@")[-1].split(":")[-1].isdigit() or ":" not in proxy or "@" not in proxy:
                format_issues.append(proxy)
            elif not test_proxy(proxy):
                http_issues.append(proxy)
            else:
                valid_proxies.append(proxy)

    if format_issues:
        log.message(f"Error", f"Invalid proxy format for the following proxies: {', '.join(format_issues)}")
        log.message("Info", "The correct proxy format is user:pass@ip:port")

    if http_issues:
        log.message("Error", f"Request issue for the following proxies: {', '.join(http_issues)}")
        log.message("Info", "The problem might be that the proxy is not working. You can try using a different proxy or buying more bandwith if you use a bandwith subscription proxy.")
        
    
    with open('proxies.txt', 'w') as f:
        for proxy in valid_proxies:
            f.write(proxy + '\n')
    
    if format_issues or http_issues:
        exit_message()

if PROXY_CHECKER:
    check_proxies(proxies)

# ------------------------------ SCRIPT ABOVE WORKING BUT UNDER CONSTRUCTION ------------------------------ #

# Ask user for message
message = log.question(f"Enter the message you want to send: ")
try:
    threads_count = int(log.question(f"Enter the number of threads to use: "))
except Exception:
    threads_count = 10  # Base Threads

home()

# Send message to all available channels and DMs
def send_message(token, used_tokens):
    session = requests.Session()
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    proxy = random.choice(proxies)
    session.proxies = {
        'http': "http://" + proxy,
        'https': "http://" + proxy
    }

    try:
        response = session.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
        if response.status_code == 401:
            log.failure(f"Invalid token: {truncate_token(token)}")
            with open('invalid.txt', 'a') as f:
                f.write(token + '\n')
            TOKEN.remove(token)
            with open('tokens.txt', 'w') as f:
                for token in TOKEN:
                    f.write(token + '\n')
            return
        elif response.status_code == 429:
            log.failure(f"Rate limited for token: {truncate_token(token)} {response.text}")
        elif response.status_code != 200 and DEBUG:
            log.failure(f"Failed to get guilds for token {truncate_token(token)}: {response.status_code} - {response.text}")
            

        guilds = json.loads(response.text)

        for guild in guilds:
            response = session.get(f'https://discord.com/api/v9/guilds/{guild["id"]}/channels', headers=headers)
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
                    if (channel["id"], guild["id"]) in used_tokens:
                        continue
                    
                    req1 = session.post(f'https://discord.com/api/v9/channels/{channel["id"]}/messages', headers=headers, json={'content': message})
                 
                    if req1.status_code == 200 and DETAILED:
                        log.message("Success", f"Successfully sent message to {channel['name']} in {guild['name']} {truncate_token(token)}")
                    elif req1.status_code == 401:
                        log.failure(f"Invalid token: {truncate_token(token)}")
                        with open('invalid.txt', 'a') as f:
                            f.write(token + '\n')
                        TOKEN.remove(token)
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

                    used_tokens.add((channel["id"], guild["id"]))

        response = session.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
        if response.status_code == 401:
            log.failure(f"Invalid token: {truncate_token(token)}")
            with open('invalid.txt', 'a') as f:
                f.write(token + '\n')
            TOKEN.remove(token)
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
                if dm['recipients'][0]['bot']:
                    continue
                if dm["id"] in used_tokens:
                    continue
                req1 = session.post(f'https://discord.com/api/v9/channels/{dm["id"]}/messages', headers=headers, json={'content': message})
                if req1.status_code == 200 and DETAILED:
                    log.message("Success", f"Successfully sent message to DM {dm['name']} {truncate_token(token)}")
                elif req1.status_code == 401:
                    log.failure(f"Invalid token: {truncate_token(token)}")
                    with open('invalid.txt', 'a') as f:
                        f.write(token + '\n')
                    TOKEN.remove(token)
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

                used_tokens.add(dm["id"])

    except Exception as e:
        if DEBUG:
            print(e)

used_tokens = set()

with ThreadPoolExecutor(max_workers=threads_count) as executor:
    futures = [executor.submit(send_message, token, used_tokens) for token in TOKEN]

for future in futures:
    future.result()
