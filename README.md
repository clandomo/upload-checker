# TMDb Torrent Search Script

This script is designed to search for torrents across multiple sites using TMDb IDs. It provides functionality to either specify a TMDb ID manually or read from a `.json` file containing multiple TMDb IDs. The script checks whether torrents corresponding to these IDs are available on various torrent sites and outputs the results in an organized format.

## Features

- **Search Modes**: Choose between Movies or Shows, and specify a TMDb ID manually or read from a `.json` file.
- **Multi-Site Support**: Search for torrents on multiple torrent sites including BLU, ATH, ULCX, LST, and FNP.
- **TMDb Data Handling**: Automatically download the latest TMDb IDs file if it is missing or empty, and remove processed entries from the `.json` file to avoid redundant searches.
- **Detailed Output**: Get organized results with media name, file size, media type, and resolution.
- **Error Handling**: Includes robust error handling and user prompts to guide through the process.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `requests`
  - `tqdm`
  - `colorama`
  - `pytz`

Install the required packages using pip:

```sh
pip3 install --user -U -r requirements.txt
```

## Setup

1. Clone the repository.
2. Place your site's API keys in the `api_keys` dictionary within the script.
3. Ensure that your `.json` files containing TMDb IDs (`movies_tmdb_ids.json` and `shows_tmdb_ids.json`) are in the same directory as the script.
> [!NOTE]
> If the appropriate `.json` files are not found, the script will generate an error and provide an option to download them directly through the script. This is recommended, as it ensures that the correct and most recent export from TMDb is downloaded and properly renamed for use.

## Usage

### Running the Script

1. **Select Search Type**: Upon running the script, you will be prompted to choose whether you want to search for Movies or Shows.

2. **Specify Search Mode**: You can choose to either:
   - **Specify a TMDb ID manually**: Enter a TMDb ID, and the script will search for it across the supported torrent sites.
   - **Read from a `.json` file**: The script will read TMDb IDs from the corresponding `.json` file and process them.

3. **Search Execution**: The script will search for torrents that match the TMDb ID(s) and display results, including:
   - Media name
   - File size (in GiB)
   - Media type (e.g., Remux, WEB-DL)
   - Resolution (e.g., 1080p, 2160p)

4. **Post-Search Options**: After the search, you can choose to remove the processed TMDb ID(s) from the `.json` file to avoid future redundant searches.

### Example

```sh
python check-upload.py
```

1. **Choose Search Type**: `Movies` or `Shows`.
2. **Choose Search Mode**: `id` or `json`.
3. **Specify TMDb ID (if in `id` mode)**: Enter the TMDb ID you'd like to search for.

### Handling Missing or Empty `.json` Files

If the script detects that the `.json` file is empty or missing, it will prompt you to download the latest TMDb IDs file. The file is downloaded based on the current date to ensure the most up-to-date information.

## API Keys

Make sure you have valid API keys for the supported torrent sites. Without these keys, the script will return "No data found" for those sites.

## Error Handling

The script includes error handling for:
- Missing API keys
- Invalid TMDb IDs
- Network issues while fetching torrent data
- Issues with downloading or processing the TMDb IDs `.json` file

## Contributing

If you have suggestions or want to contribute, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/MIT) file for details.

---

### Additional Notes

- Ensure you follow the API usage guidelines of the supported torrent sites to avoid rate limiting or being banned.
- The script is designed to be user-friendly, with prompts and feedback to guide you through the search process.