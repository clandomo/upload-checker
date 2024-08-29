import time
import pytz
import requests
from api_manager import send_request
from datetime import datetime, timedelta
from colorama import Fore, Style
from tqdm import tqdm

def output_site_results(progress_bar, site_results):
    if progress_bar is None:
        for site_name, results in site_results.items():
            print(Fore.YELLOW + Style.BRIGHT + f"{site_name}:")
            for result in results:
                print(Fore.WHITE + f"  {result}")
            print('\n')
    else:
        for site_name, results in site_results.items():
            progress_bar.write(Fore.YELLOW + Style.BRIGHT + f"{site_name}:")
            for result in results:
                progress_bar.write(Fore.WHITE + f"  {result}")
            progress_bar.write('\n')

def bytes_to_gib(size_in_bytes):
    return size_in_bytes / (1024 ** 3)

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
    
def fetch_site_data(progress_bar, sites, params, search_type):
    site_results = {}

    for site_name, site_info in sites.items():
        try:
            # Send request to site for torrent infromation
            sites[site_name]['response'] = send_request(site_name, site_info, params)

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
            if progress_bar is None:
                print(Fore.RED + Style.BRIGHT + f"Error fetching data from {site_name}: {str(e)}")
            else:
                progress_bar.write(Fore.RED + Style.BRIGHT + f"Error fetching data from {site_name}: {str(e)}")
            site_results[site_name] = [f"Error fetching data: {str(e)}"]
            continue
    
    return site_results

def extract_tmdb_ids_titles(tmdb_entries, search_type):
    if search_type == 'movies':
        return [(entry['id'], entry.get('original_title', 'Unknown Title')) for entry in tmdb_entries]
    elif search_type == 'shows':
        return [(entry['id'], entry.get('original_name', 'Unknown Title')) for entry in tmdb_entries]