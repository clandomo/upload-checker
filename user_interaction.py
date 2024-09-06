from file_manager import download_and_extract_tmdb_ids
from rich.console import Console

console = Console()

def get_iterations(max_iterations):
    while True:
        try:
            console.print(f"[bold bright_yellow]Enter the number of iterations you'd like to perform (Max {max_iterations}):[/] ", end="")
            iterations = int(input())
            
            if iterations <= 0:
                console.print("[bold bright_red]Please enter a positive number greater than 0.[/]")
            elif iterations > max_iterations:
                console.print(f"[bold bright_red]Please enter a number less than or equal to {max_iterations}.[/]")
            elif iterations > 50:
                console.print("[underline bold bright_yellow]WARNING: Doing more than 50 iterations can cause issues. Type 'confirm' to proceed or 'back' to change the number: ")
                warning = input().lower()
                if warning == 'confirm':
                    return iterations
                elif warning != 'back':
                    console.print("[underline bold bright_red]Invalid input. Please type 'confirm' or 'back'.[/]")
            else:
                return iterations
                
        except ValueError:
            console.print("[bold bright_red]Please enter a valid positive integer.[/]")

def get_search_type():
    while True:
        console.print("[bold bright_yellow]Would you like to search for Movies or Shows? [/]", end="")
        search_type = input().strip().lower()
        if search_type in ['movies', 'shows']:
            return search_type
        else:
            console.print("[underline bold bright_red]Invalid input. Please enter 'Movies' or 'Shows'.[/]")

def get_tmdb_mode():
    while True:
        console.print("[bold bright_yellow]Would you like to specify a TMDb ID or read from the '.json' file? (type 'id' or 'json'): [/]", end="")
        mode = input().strip().lower()
        if mode in ['id', 'json']:
            return mode
        else:
            console.print("[bold bright_red]Invalid input. Please type 'id' to specify a TMDb ID or 'json' to read from the '.json' file.[/]")

def get_tmdb_file(search_type, download_url, filepath, load_tmdb_ids):
    console.print(f"[underline bold bright_red]The {search_type.capitalize()} TMDb IDs file is either empty or missing. Please download a new file.[/]")
    while True:
        console.print("[bold bright_yellow]Would you like to download the latest TMDb IDs file? (Y/N): [/]", end="")
        download = input().strip().lower()
        if download == 'y':
            download_and_extract_tmdb_ids(download_url, filepath)
            tmdb_entries = load_tmdb_ids(filepath)
            if not tmdb_entries:
                console.print(f"[underline bold bright_red]ERROR: Failed to download or load the {search_type.capitalize()} TMDb IDs file. Exiting...[/]")
                exit(1)
            break
        elif download == 'n':
            console.print("[bold bright_red]Exiting script...[/]")
            exit(1)
        else:
            console.print("[bold bright_red]Invalid input. Please type 'Y' or 'N'.[/]")
    return tmdb_entries

def removed_parsed_entries():
    while True:
        console.print("[bold bright_yellow]Would you like to remove the recently parsed TMDb ID(s) from the '.json' file? (yes/no): [/]", end="")
        answer = input().strip().lower()
        if answer == 'yes':
            return True
        elif answer == 'no':
            return False
        else:
            console.print("[bold bright_red]Invalid input. Please type 'yes' or 'no'.[/]")