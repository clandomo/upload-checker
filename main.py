import time
import requests
import random

from api_manager import validate_config, load_config, setup_api_keys_and_sites, test_api_key
from file_manager import load_tmdb_ids, save_tmdb_ids, get_tmdb_filepath_and_entries
from user_interaction import get_iterations, get_search_type, get_tmdb_mode, get_tmdb_file, removed_parsed_entries
from utils import get_latest_tmdb_url, fetch_site_data, extract_tmdb_ids_titles, output_site_results
from tqdm import tqdm
from colorama import Back, Fore, Style, init

# Initialize colorama (required for Windows)
init(autoreset=True)

# Load the configuration
config = load_config()

# Validate the configuration
validate_config(config)

# Configure API and site information
api_keys, sites = setup_api_keys_and_sites(config)

# List to store site names where the API check fails
failed_sites = []

# Test API keys from config.json
for site_name, site_info in sites.items():
    if test_api_key(site_info['url'], site_info['headers']):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"The API key for {site_name} is valid.")    
    else:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"WARNING: The API key for {site_name} is invalid or there was an error.")
        failed_sites.append(site_name)

# Check if all sites failed
if len(failed_sites) == len(sites):
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "ERROR: All API keys failed. The script cannot proceed. Exiting script...")
    exit(1)

# Determine the search type (Movies or Shows)
search_type = get_search_type()

# Load the appropriate TMDb IDs file based on the user's choice
filepath, tmdb_entries = get_tmdb_filepath_and_entries(search_type)

# Get the latest URL for downloading TMDb IDs
download_url = get_latest_tmdb_url(search_type)

# Check if the file is empty or contains no valid TMDb IDs
if not tmdb_entries:
    tmdb_entries = get_tmdb_file(search_type, download_url, filepath, load_tmdb_ids)

# Ask the user if they want to specify a TMDb ID or read from the .json file
mode = get_tmdb_mode()

if mode == 'json':
    # Shuffle the entries to randomize the order
    random.shuffle(tmdb_entries)

    # Extract IDs and titles for processing
    tmdb_ids_titles = extract_tmdb_ids_titles(tmdb_entries, search_type)

    # List to track which IDs were successfully processed
    processed_tmdb_ids = []

    # Get the number of iterations the user wants to perform
    iterations = get_iterations(len(tmdb_ids_titles))

    # Create progress bar
    progress_bar = tqdm(
        range(iterations),
        desc=Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Checking TMDb IDs" + Style.RESET_ALL, 
        bar_format="{l_bar}%s{bar}%s" % (Fore.LIGHTGREEN_EX + Back.LIGHTRED_EX, Style.RESET_ALL) + 
        Fore.LIGHTYELLOW_EX + Style.BRIGHT + "[Elapsed: {elapsed} | Remaining: {remaining}]" + Style.RESET_ALL
    )

    # Perform the checks
    for i in progress_bar:

        tmdb_id, title = tmdb_ids_titles[i]
        params = {'tmdbId': tmdb_id}

        progress_bar.write(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"Searching for TMDb ID: {tmdb_id} (Title: {title})")
        
        site_results = fetch_site_data(progress_bar, sites, params, search_type, failed_sites)

        # Output results in organized format
        output_site_results(progress_bar, site_results)

        # Add the processed TMDb ID to the list
        processed_tmdb_ids.append(tmdb_id)

elif mode == 'id':
    while True:
        # Ask for the specific TMDb ID(s)
        tmdb_ids_input = input(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Enter the TMDb ID(s) you'd like to search for (comma-separated if multiple): ").strip()

        # Split the input into a list of TMDb IDs, strip whitespace, and remove duplicates by converting to a set
        tmdb_ids = {tmdb_id.strip() for tmdb_id in tmdb_ids_input.split(',')}

        # Convert the set back to a list of integers for comparison
        try:
            tmdb_ids = [int(tmdb_id) for tmdb_id in tmdb_ids]
            break  # If conversion succeeds, break out of the loop
        except ValueError:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + "ERROR: All TMDb IDs must be numeric values. Please also ensure there are no leading or trailing commas.")

    # Extract IDs and titles for processing
    tmdb_ids_titles = extract_tmdb_ids_titles(tmdb_entries, search_type)

    # List to track which IDs were successfully processed
    processed_tmdb_ids = []

    # Get the number of iterations based on how many TMDb IDs user inputs
    iterations = len(tmdb_ids)

    # Create progress bar
    progress_bar = tqdm(
        range(iterations),
        desc=Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Checking TMDb IDs" + Style.RESET_ALL, 
        bar_format="{l_bar}%s{bar}%s" % (Fore.LIGHTGREEN_EX + Back.LIGHTRED_EX, Style.RESET_ALL) + 
        Fore.LIGHTYELLOW_EX + Style.BRIGHT + "[Elapsed: {elapsed} | Remaining: {remaining}]" + Style.RESET_ALL
    )


    # Perform the checks
    for i in progress_bar:

        tmdb_id = tmdb_ids[i]
        found_entry = next((entry for entry in tmdb_ids_titles if entry[0] == tmdb_id), None)

        if found_entry:
            tmdb_id, title = found_entry
            progress_bar.write(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"Found TMDb ID: {tmdb_id} (Title: {title})")
            params = {'tmdbId': tmdb_id}

            site_results = fetch_site_data(progress_bar, sites, params, search_type, failed_sites)

            # Output results in organized format
            output_site_results(progress_bar, site_results)

            # Add the processed TMDb ID to the list
            processed_tmdb_ids.append(tmdb_id)
        else:
            progress_bar.write(Fore.LIGHTRED_EX + Style.BRIGHT + f"ERROR: TMDb ID {tmdb_id} not found in the {search_type.capitalize()} TMDb IDs file.")


# After processing all TMDb IDs, ask whether to remove them from the .json file
if processed_tmdb_ids:
    remove_items = removed_parsed_entries()

    if remove_items:
        # Remove processed entries from the list and save the remaining entries back to the file
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Removing TMDb ID(s) that have already been searched from the `.json` file to maintain a list of unsearched IDs.")
        tmdb_entries = [entry for entry in tmdb_entries if entry['id'] not in processed_tmdb_ids]  # Remove processed entries
        save_tmdb_ids(filepath, tmdb_entries)
    else:
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "TMDb ID entry/entries will remain in the `.json` file and will not be removed.")