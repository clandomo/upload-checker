from colorama import Fore, Style
from file_manager import download_and_extract_tmdb_ids

def get_iterations(max_iterations):
    while True:
        try:
            iterations = int(input(Fore.YELLOW + Style.BRIGHT + f"Enter the number of iterations you'd like to perform (Max {max_iterations}): "))
            
            if iterations <= 0:
                print(Fore.RED + Style.BRIGHT + "Please enter a positive number greater than 0.")
            elif iterations > max_iterations:
                print(Fore.RED + Style.BRIGHT + f"Please enter a number less than or equal to {max_iterations}.")
            elif iterations > 50:
                warning = input(Fore.RED + Style.BRIGHT + "WARNING: Doing more than 50 iterations can cause issues. Type 'confirm' to proceed or 'back' to change the number: ").lower()
                if warning == 'confirm':
                    return iterations
                elif warning != 'back':
                    print(Fore.RED + Style.BRIGHT + "Invalid input. Please type 'confirm' or 'back'.")
            else:
                return iterations
                
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Please enter a valid positive integer.")



def get_search_type():
    while True:
        search_type = input(Fore.YELLOW + Style.BRIGHT + "Would you like to search for Movies or Shows? ").strip().lower()
        if search_type in ['movies', 'shows']:
            return search_type
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid input. Please enter 'Movies' or 'Shows'.")

def get_tmdb_mode():
    while True:
        mode = input(Fore.YELLOW + Style.BRIGHT + "Would you like to specify a TMDb ID or read from the '.json' file? (type 'id' or 'json'): ").strip().lower()
        if mode in ['id', 'json']:
            return mode
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid input. Please type 'id' to specify a TMDb ID or 'json' to read from the '.json' file.")

def get_tmdb_file(search_type, download_url, filepath, load_tmdb_ids):
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