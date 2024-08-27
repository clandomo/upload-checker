import requests
import random
from tqdm import tqdm
from colorama import Fore, Style, init

# EDIT HERE
blu_api_key = "INSERT BLU API KEY HERE"
ath_api_key = "INSERT ATH API KEY HERE"

# Initialize colorama (required for Windows)
init(autoreset=True)

def get_iterations():
    while True:
        try:
            iterations = int(input(Fore.YELLOW + Style.BRIGHT + "Enter the number of iterations you'd like to perform: "))
            if iterations > 50:
                warning = input(Fore.RED + Style.BRIGHT + "WARNING: Doing more than 50 iterations can cause issues. Type 'confirm' to proceed or 'back' to change the number: ").lower()
                if warning == 'confirm':
                    break
                elif warning == 'back':
                    continue
                else:
                    print(Fore.YELLOW + "Invalid input. Please type 'confirm' or 'back'.")
            else:
                break
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Please enter a valid number.")
    return iterations

iterations = get_iterations()

# URLs and headers for the APIs
blu_url = "https://blutopia.cc/api/torrents/filter"
ath_url = "https://aither.cc/api/torrents/filter"

blu_headers = {
    'Authorization': f'Bearer {blu_api_key}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

ath_headers = {
    'Authorization': f'Bearer {ath_api_key}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Create a styled progress bar
for i in tqdm(range(iterations), desc=Fore.YELLOW + Style.BRIGHT + "Checking TMDb IDs" + Style.RESET_ALL, 
              bar_format="{l_bar}%s{bar}%s [Elapsed: {elapsed} | Remaining: {remaining}]" % (Fore.CYAN, Fore.RESET)):
    params = {
        'tmdbId': random.randint(0, 999999)
    }
    blu_response = requests.get(blu_url, headers=blu_headers, params=params)
    ath_response = requests.get(ath_url, headers=ath_headers, params=params)
    blu_response = blu_response.json()
    ath_response = ath_response.json()

    try:
        if len(blu_response.get('data', [])) == 0 and len(ath_response.get('data', [])) != 0:
            movie_name = ath_response['data'][0]['attributes']['name']
            tqdm.write(Fore.YELLOW + Style.BRIGHT + "ATH has data but BLU does not: " + Fore.WHITE + f"{movie_name}" + '\n')
        elif len(blu_response.get('data', [])) != 0 and len(ath_response.get('data', [])) == 0:
            movie_name = blu_response['data'][0]['attributes']['name']
            tqdm.write(Fore.YELLOW + Style.BRIGHT + "BLU has data but ATH does not: " + Fore.WHITE + f"{movie_name}" + '\n')
    except Exception as e:
        if 'message' in blu_response:
            tqdm.write(Fore.RED + Style.BRIGHT + f"Error from BLU: {blu_response['message']}" + '\n')
        elif 'message' in ath_response:
            tqdm.write(Fore.RED + Style.BRIGHT + f"Error from ATH: {ath_response['message']}" + '\n')
        else:
            tqdm.write(Fore.RED + Style.BRIGHT + f"An error occurred: {e}" + '\n')