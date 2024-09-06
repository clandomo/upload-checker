import time
import pytz
import requests

from api_manager import send_request
from file_manager import save_json_response
from datetime import datetime, timedelta
from rich.console import Console
from rich.text import Text

console = Console()

def output_site_results(site_results):
    for site_name, results in site_results.items():
        # Print the site name in bold yellow
        console.print(f"[bold bright_yellow]{site_name}:[/]")
        
        # Iterate through the results (which are Text objects) and print them directly
        for result in results:
            console.print(result)  
        console.print()  # Print a blank line for spacing

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
    
def fetch_site_data(sites, params, search_type, failed_sites):
    site_results = {}

    for site_name, site_info in sites.items():
        if site_name in failed_sites:
            continue  # Skip the site if it's in the failed_sites list

        try:
            # Send request to site for torrent information
            sites[site_name]['response'] = send_request(site_name, site_info, params)

            # Save the JSON response to a file for inspection (DEBUG ONLY)
            #save_json_response(site_name, sites[site_name]['response'])

            if sites[site_name]['response'] and 'data' in sites[site_name]['response']:
                sites[site_name]['has_data'] = True
                site_results[site_name] = []
                for item in sites[site_name]['response'].get('data', []):
                    # Define valid categories based on the search type
                    valid_categories = {
                        'movies': ["movie", "movies"],
                        'shows': ["tv show", "tv shows", "tv"]
                    }

                    category = item['attributes'].get('category', '').lower()

                    # Check if the category is valid for the search type
                    if category in valid_categories.get(search_type, []):
                        media_name = item['attributes'].get('name', 'Unknown')
                    else:
                        continue  # Skip entries that do not match the search type
                    
                    media_type = item['attributes'].get('type', 'Unknown')
                    resolution = item['attributes'].get('resolution', 'Unknown')
                    size_in_bytes = item['attributes'].get('size', 0)
                    size_in_gib = bytes_to_gib(size_in_bytes)
                    seeders = item['attributes'].get('seeders', 'Unknown')
                    leechers = item['attributes'].get('leechers', 'Unknown')
                    freeleech = item['attributes'].get('freeleech', 'Unknown')

                    # Check if torrent is freelech or if value is defined in .json
                    is_freeleech = freeleech != "0%" and freeleech != "Unknown"
                    freeleech_star = f" ⭐ {freeleech}" if is_freeleech else ""

                    # Assuming site_results is a dictionary or list
                    result = Text()
                    result.append(f"{media_name}", style="bold bright_green")
                    result.append(" ➤ ", style="bright_white")
                    result.append(f"{size_in_gib:.2f} GiB {media_type} ({resolution}) S-{seeders}/L-{leechers}{freeleech_star}", style="bold bright_yellow")

                    # Storing the result in a dictionary/list
                    site_results[site_name].append(result)

            # If no relevant entries found, add "No data found"
            if not site_results.get(site_name):
                result = Text()
                result.append("No data found", style="bold bright_red")
                site_results[site_name].append(result)
        except requests.exceptions.RequestException as e:
            console.print(f"[bold bright_red]Error fetching data from {site_name}: {str(e)}[/]")
            site_results[site_name] = [f"Error fetching data: {str(e)}"]
            continue
    
    return site_results

def extract_tmdb_ids_titles(tmdb_entries, search_type):
    if search_type == 'movies':
        return [(entry['id'], entry.get('original_title', 'Unknown Title')) for entry in tmdb_entries]
    elif search_type == 'shows':
        return [(entry['id'], entry.get('original_name', 'Unknown Title')) for entry in tmdb_entries]