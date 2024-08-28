import requests
from tqdm import tqdm
from colorama import Fore, Style, init
import os
import json
import time
from datetime import datetime, timedelta
import gzip
import shutil
import pytz

# Initialize colorama (required for Windows)
init(autoreset=True)

"""
__        ___    ____  _   _ ___ _   _  ____ 
\ \      / / \  |  _ \| \ | |_ _| \ | |/ ___|
 \ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _ 
  \ V  V / ___ \|  _ <| |\  || || |\  | |_| |
   \_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____|

"""

# If an API key is not provided for any of 
# these sites, the script will consistently 
# return the value "No data found."

# API keys (EDIT HERE)
api_keys = {
    'BLU': "INSERT API KEY HERE FOR SITE",
    'ATH': "INSERT API KEY HERE FOR SITE",
    'ULCX': "INSERT API KEY HERE FOR SITE",
    'LST': "INSERT API KEY HERE FOR SITE",
    'FNP': "INSERT API KEY HERE FOR SITE"
}

# URLs and headers for the APIs
sites = {
    'BLU': {
        'url': "https://blutopia.cc/api/torrents/filter",
        'headers': {
            'Authorization': f'Bearer {api_keys["BLU"]}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        'response': None,
        'has_data': False
    },
    'ATH': {
        'url': "https://aither.cc/api/torrents/filter",
        'headers': {
            'Authorization': f'Bearer {api_keys["ATH"]}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        'response': None,
        'has_data': False
    },
    'ULCX': {
        'url': "https://upload.cx/api/torrents/filter",
        'headers': {
            'Authorization': f'Bearer {api_keys["ULCX"]}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        'response': None,
        'has_data': False
    },
    'LST': {
        'url': "https://lst.gg/api/torrents/filter",
        'headers': {
            'Authorization': f'Bearer {api_keys["LST"]}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        'response': None,
        'has_data': False
    },
    'FNP': {
        'url': "https://fearnopeer.com/api/torrents/filter",
        'headers': {
            'Authorization': f'Bearer {api_keys["FNP"]}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        'response': None,
        'has_data': False
    }
}

def load_tmdb_ids(filepath):
    tmdb_ids = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    tmdb_ids.append(data)  # Keep entire entry for later use
                except json.JSONDecodeError:
                    print(Fore.RED + Style.BRIGHT + f"ERROR: Failed to decode JSON for line: {line}")
    except FileNotFoundError:
        print(Fore.RED + Style.BRIGHT + f"ERROR: File {filepath} not found.")
    return tmdb_ids

def save_tmdb_ids(filepath, tmdb_ids):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            for entry in tmdb_ids:
                file.write(json.dumps(entry, ensure_ascii=False) + '\n')
        print(Fore.GREEN + Style.BRIGHT + f"Successfully saved TMDb IDs to {filepath}")
    except IOError as e:
        print(Fore.RED + Style.BRIGHT + f"ERROR: Failed to save TMDb IDs to {filepath}. {str(e)}")

def download_and_extract_tmdb_ids(url, output_file):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            gz_file = output_file + ".gz"
            with open(gz_file, 'wb') as file:
                file.write(response.content)
            with gzip.open(gz_file, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(gz_file)
            print(Fore.GREEN + Style.BRIGHT + f"Successfully downloaded and extracted {output_file}")
        else:
            print(Fore.RED + Style.BRIGHT + f"ERROR: Failed to download file from {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f"ERROR: Failed to download file from {url}. Exception: {str(e)}")

def get_iterations(max_iterations):
    while True:
        try:
            iterations = int(input(Fore.YELLOW + Style.BRIGHT + f"Enter the number of iterations you'd like to perform (Max {max_iterations}): "))
            if iterations > max_iterations:
                print(Fore.RED + Style.BRIGHT + f"Please enter a number less than or equal to {max_iterations}. There are only {max_iterations} left in the '.json' file.")
            elif iterations > 50:
                warning = input(Fore.RED + Style.BRIGHT + "WARNING: Doing more than 50 iterations can cause issues. Type 'confirm' to proceed or 'back' to change the number: ").lower()
                if warning == 'confirm':
                    return iterations
                elif warning == 'back':
                    continue
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "Invalid input. Please type 'confirm' or 'back'.")
            else:
                return iterations
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Please enter a valid number.")

def bytes_to_gib(size_in_bytes):
    return size_in_bytes / (1024 ** 3)

def get_search_type():
    while True:
        search_type = input(Fore.YELLOW + Style.BRIGHT + "Would you like to search for Movies or Shows? ").strip().lower()
        if search_type in ['movies', 'shows']:
            return search_type
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid input. Please enter 'Movies' or 'Shows'.")

def get_latest_tmdb_url(search_type):
    current_time_utc = datetime.now(pytz.utc)
    release_time = current_time_utc.replace(hour=8, minute=0, second=0, microsecond=0)

    if current_time_utc < release_time:
        date_for_url = (current_time_utc - timedelta(days=1)).strftime('%m_%d_%Y')
    else:
        date_for_url = current_time_utc.strftime('%m_%d_%Y')

    if search_type == 'movies':
        return f"http://files.tmdb.org/p/exports/movie_ids_{date_for_url}.json.gz"
    else:
        return f"http://files.tmdb.org/p/exports/tv_series_ids_{date_for_url}.json.gz"

def get_tmdb_mode():
    while True:
        mode = input(Fore.YELLOW + Style.BRIGHT + "Would you like to specify a TMDb ID or read from the '.json' file? (type 'id' or 'json'): ").strip().lower()
        if mode in ['id', 'json']:
            return mode
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid input. Please type 'id' to specify a TMDb ID or 'json' to read from the '.json' file.")

def get_tmdb_file():
    print(Fore.RED + Style.BRIGHT + f"ERROR: The {search_type.capitalize()} TMDb IDs file is either empty or missing. Please download a new file.")
    while True:
        download = input(Fore.YELLOW + Style.BRIGHT + "Would you like to download the latest TMDb IDs file? (yes/no): ").strip().lower()
        if download == 'yes':
            download_and_extract_tmdb_ids(download_url, filepath)
            tmdb_entries = load_tmdb_ids(filepath)
            if not tmdb_entries:
                print(Fore.RED + Style.BRIGHT + f"ERROR: Failed to download or load the {search_type.capitalize()} TMDb IDs file. Exiting...")
                exit(1)
            break
        elif download == 'no':
            print(Fore.RED + Style.BRIGHT + "Exiting script...")
            exit(1)
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid input. Please type 'yes' or 'no'.")
    return tmdb_entries

def removed_parsed_entries():
    while True:
        answer = input(Fore.YELLOW + Style.BRIGHT + "Would you like to remove the recently parsed TMDb ID(s) from the '.json' file? (yes/no): ").strip().lower()
        if answer == 'yes':
            return True
        elif answer == 'no':
            return False
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid input. Please type 'yes' or 'no'.")

"""
def save_json_response(site_name, response_data):
    filename = f"{site_name}_response.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(response_data, file, ensure_ascii=False, indent=4)
    print(Fore.GREEN + Style.BRIGHT + f"Saved {site_name} response to {filename}")
"""

# Determine the search type (Movies or Shows)
search_type = get_search_type()

# Load the appropriate TMDb IDs file based on the user's choice
if search_type == 'movies':
    filepath = 'movies_tmdb_ids.json'
else:
    filepath = 'shows_tmdb_ids.json'

# Get the latest URL for downloading TMDb IDs
download_url = get_latest_tmdb_url(search_type)

# Ask the user if they want to specify a TMDb ID or read from the .json file
mode = get_tmdb_mode()

if mode == 'json':
    tmdb_entries = load_tmdb_ids(filepath)

    # Check if the file is empty or contains no valid TMDb IDs
    if not tmdb_entries:
        tmdb_entries = get_tmdb_file()

    # Extract IDs and titles for processing, if statement needed as .json has different labels for title
    if search_type == 'movies':
        tmdb_ids_titles = [(entry['id'], entry.get('original_title', 'Unknown Title')) for entry in tmdb_entries]
    elif search_type == 'shows':
        tmdb_ids_titles = [(entry['id'], entry.get('original_name', 'Unknown Title')) for entry in tmdb_entries]

    # Get the number of iterations the user wants to perform
    iterations = get_iterations(len(tmdb_ids_titles))

    # Perform the checks
    for i in tqdm(range(iterations), desc=Fore.YELLOW + Style.BRIGHT + "Checking TMDb IDs" + Style.RESET_ALL, 
                  bar_format="{l_bar}%s{bar}%s [Elapsed: {elapsed} | Remaining: {remaining}]" % (Fore.CYAN, Fore.RESET)):

        tmdb_id, title = tmdb_ids_titles[i]
        params = {'tmdbId': tmdb_id}

        tqdm.write(Fore.YELLOW + Style.BRIGHT + f"Searching for TMDb ID: {tmdb_id} (Title: {title})")
        
        # Request data from each site and store the responses
        site_results = {}
        for site_name, site_info in sites.items():
            try:
                response = requests.get(site_info['url'], headers=site_info['headers'], params=params)
                sites[site_name]['response'] = response.json()

                # Add a delay between requests to avoid rate limit
                time.sleep(1)

                """
                # Save the JSON response to a file for inspection
                save_json_response(site_name, sites[site_name]['response'])
                """

                if sites[site_name]['response'] and 'data' in sites[site_name]['response']:
                    sites[site_name]['has_data'] = True
                    site_results[site_name] = []
                    for item in sites[site_name]['response'].get('data', []):
                        # Check if the category is "Movie", "Movies", or "TV Show", "TV Shows" based on search type
                        category = item['attributes'].get('category', '').lower()
                        if search_type == 'movies' and category in ["movie", "movies"]:
                            media_name = item['attributes'].get('name', 'Unknown')
                        elif search_type == 'shows' and category in ["tv show", "tv shows", "tv"]:
                            media_name = item['attributes'].get('name', 'Unknown')
                        else:
                            continue  # Skip entries that do not match the search type
                        
                        media_type = item['attributes'].get('type', 'Unknown')
                        resolution = item['attributes'].get('resolution', 'Unknown')
                        size_in_bytes = item['attributes'].get('size', 0)
                        size_in_gib = bytes_to_gib(size_in_bytes)
                        site_results[site_name].append(f"{media_name} | {size_in_gib:.2f} GiB {media_type} ({resolution})")
                # If no relevant entries found, add "No data found"
                if not site_results.get(site_name):
                    site_results[site_name] = ["No data found"]
            except requests.exceptions.RequestException as e:
                tqdm.write(Fore.RED + Style.BRIGHT + f"Error fetching data from {site_name}: {str(e)}")
                site_results[site_name] = [f"Error fetching data: {str(e)}"]
                continue
        
        # Output results in organized format
        for site_name, results in site_results.items():
            tqdm.write(Fore.YELLOW + Style.BRIGHT + f"{site_name}:")
            for result in results:
                tqdm.write(Fore.WHITE + f"  {result}")
            tqdm.write('\n')

    # Decide whether to keep or remove TMDb IDs that were searched
    remove_items = removed_parsed_entries()

    if (remove_items == True):
        # Remove processed entries from the list and save the remaining entries back to the file
        print(Fore.YELLOW + Style.BRIGHT + "Removing TMDb ID(s) that have already been searched from the `.json` file to maintain a list of unsearched IDs.")
        tmdb_entries = tmdb_entries[iterations:]  # Remove processed entries
        save_tmdb_ids(filepath, tmdb_entries)
    else:
        print(Fore.YELLOW + Style.BRIGHT + "TMDb ID entry/entries will remain in the `.json` file and will not be removed.")

elif mode == 'id':
    tmdb_entries = load_tmdb_ids(filepath)

    # Check if the file is empty or contains no valid TMDb IDs
    if not tmdb_entries:
        tmdb_entries = get_tmdb_file()

    # Ask for the specific TMDb ID
    tmdb_id = input(Fore.YELLOW + Style.BRIGHT + "Enter the specific TMDb ID you'd like to search for: ").strip()

    # Convert tmdb_id to an integer for comparison, if applicable
    try:
        tmdb_id = int(tmdb_id)
    except ValueError:
        print(Fore.RED + Style.BRIGHT + "ERROR: TMDb ID should be a numeric value.")
        exit(1)

    # Extract IDs and titles for processing, and search for the entered TMDb ID
    if search_type == 'movies':
        tmdb_ids_titles = [(entry['id'], entry.get('original_title', 'Unknown Title')) for entry in tmdb_entries]
    elif search_type == 'shows':
        tmdb_ids_titles = [(entry['id'], entry.get('original_name', 'Unknown Title')) for entry in tmdb_entries]

    # Search for the TMDb ID in the list of entries
    found_entry = next((entry for entry in tmdb_ids_titles if entry[0] == tmdb_id), None)

    if found_entry:
        tmdb_id, title = found_entry
        print(Fore.GREEN + Style.BRIGHT + f"Found TMDb ID: {tmdb_id} (Title: {title})")
        params = {'tmdbId': tmdb_id}

        # Proceed with the search process
        site_results = {}
        for site_name, site_info in sites.items():
            try:
                response = requests.get(site_info['url'], headers=site_info['headers'], params=params)
                sites[site_name]['response'] = response.json()

                # Add a delay between requests to avoid rate limit
                time.sleep(1) 

                """
                # Save the JSON response to a file for inspection
                save_json_response(site_name, sites[site_name]['response'])
                """

                # Check if the site has data that meets the conditions
                if sites[site_name]['response'] and 'data' in sites[site_name]['response']:
                    sites[site_name]['has_data'] = True
                    site_results[site_name] = []
                    for item in sites[site_name]['response'].get('data', []):
                        category = item['attributes'].get('category', '').lower()
                        if search_type == 'movies' and category in ["movie", "movies"]:
                            media_name = item['attributes'].get('name', 'Unknown')
                        elif search_type == 'shows' and category in ["tv show", "tv shows", "tv"]:
                            media_name = item['attributes'].get('name', 'Unknown')
                        else:
                            continue  # Skip entries that do not match the search type
                    
                        media_type = item['attributes'].get('type', 'Unknown')
                        resolution = item['attributes'].get('resolution', 'Unknown')
                        size_in_bytes = item['attributes'].get('size', 0)
                        size_in_gib = bytes_to_gib(size_in_bytes)
                        site_results[site_name].append(f"{media_name} | {size_in_gib:.2f} GiB {media_type} ({resolution})")
                if not site_results.get(site_name):
                    site_results[site_name] = ["No data found"]
            except requests.exceptions.RequestException as e:
                tqdm.write(Fore.RED + Style.BRIGHT + f"Error fetching data from {site_name}: {str(e)}")
                site_results[site_name] = [f"Error fetching data: {str(e)}"]
                continue
    
        # Output results in organized format
        for site_name, results in site_results.items():
            tqdm.write(Fore.YELLOW + Style.BRIGHT + f"{site_name}:")
            for result in results:
                tqdm.write(Fore.WHITE + f"  {result}")
            tqdm.write('\n')

        # Decide whether to keep or remove TMDb IDs that were searched
        remove_items = removed_parsed_entries()

        if (remove_items == True):
            # Remove processed entries from the list and save the remaining entries back to the file
            print(Fore.YELLOW + Style.BRIGHT + "Removing TMDb ID(s) that have already been searched from the `.json` file to maintain a list of unsearched IDs.")
            tmdb_entries = [entry for entry in tmdb_entries if entry['id'] != tmdb_id]  # Remove processed entry
            save_tmdb_ids(filepath, tmdb_entries)
        else:
            print(Fore.YELLOW + Style.BRIGHT + "TMDb ID entry will remain in the `.json` file and will not be removed.")
    else:
        print(Fore.RED + Style.BRIGHT + f"ERROR: TMDb ID {tmdb_id} not found in the {search_type.capitalize()} TMDb IDs file.")