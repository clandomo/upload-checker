import json
import requests
import gzip
import shutil
import os

from colorama import Fore, Style

def get_tmdb_filepath_and_entries(search_type):
    filepath = 'movies_tmdb_ids.json' if search_type == 'movies' else 'shows_tmdb_ids.json'
    tmdb_entries = load_tmdb_ids(filepath)
    return filepath, tmdb_entries

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