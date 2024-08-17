import requests
import csv
import time
import os
import argparse

def get_game_info(game_domain_name, api_key):
    """
    Retrieves information about a game from the Nexus Mods API.

    Args:
        game_domain_name (str): The domain name of the game (e.g., 'skyrimspecialedition').
        api_key (str): The API key for authentication.

    Returns:
        dict: The game information in JSON format.
    """
    url = f"https://api.nexusmods.com/v1/games/{game_domain_name}.json"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve game data: {e}")
        return None

def get_mod_info(game_domain_name, mod_id, api_key):
    """
    Retrieves information about a specific mod for a game from the Nexus Mods API.

    Args:
        game_domain_name (str): The domain name of the game (e.g., 'skyrimspecialedition').
        mod_id (int): The ID of the mod.
        api_key (str): The API key for authentication.

    Returns:
        dict: The mod information in JSON format.
    """
    url = f"https://api.nexusmods.com/v1/games/{game_domain_name}/mods/{mod_id}.json"
    headers = {"apikey": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve mod data for ID {mod_id}: {e}")
        return None

def create_category_reference_table(categories, file_name):
    """
    Creates a CSV reference table of categories from the game information.

    Args:
        categories (list): List of categories from the game information.
        file_name (str): The name of the output CSV file.
    """
    headers = ["category_id", "name", "parent_category"]

    with open(file_name, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for category in categories:
            writer.writerow({
                "category_id": category["category_id"],
                "name": category["name"],
                "parent_category": category["parent_category"] if category["parent_category"] else "None"
            })

    print(f"Category reference table saved to {file_name}")

def process_mods_from_csv(csv_file, api_key, game_domain_name, category_reference_file):
    """
    Processes a CSV file to get mod references, retrieves mod info, and compiles a summary.

    Args:
        csv_file (str): The path to the CSV file containing mod references.
        api_key (str): The API key for authentication.
        game_domain_name (str): The domain name of the game (e.g., 'skyrimspecialedition').
        category_reference_file (str): The path to the category reference CSV file.
    """
    # Load category reference from file
    categories = {}
    with open(category_reference_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            categories[int(row["category_id"])] = row["name"]

    output_file = "mod_summaries.csv"
    # Open the output file in write mode to ensure headers are written
    with open(output_file, mode="w", newline="") as file:
        fieldnames = ["name_from_file", "name_from_mod_info", "summary", "category"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    # Process the CSV file for mod references
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there is one
        for row in reader:
            if len(row) >= 3:
                mod_id = row[2]
                mod_info = get_mod_info(game_domain_name, mod_id, api_key)
                if mod_info:
                    print(f'Processing mod ID {mod_id}')
                    time.sleep(1)  # Sleep to manage rate limiting
                    # Extract relevant fields
                    mod_summary = {
                        "name_from_file": row[0],
                        "name_from_mod_info": mod_info.get("name", "N/A"),
                        "summary": mod_info.get("summary", row[1]),
                        "category": categories.get(mod_info.get("category_id"), "Unknown")
                    }

                    # Open the file in append mode to add the new mod summary
                    with open(output_file, mode="a", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writerow(mod_summary)

                    print(f"Processed and saved mod ID {mod_id}")

def main():
    parser = argparse.ArgumentParser(description="Process mods for a specific game from a CSV file.")
    parser.add_argument("game_domain_name", help="The domain name of the game (e.g., 'skyrimspecialedition').")
    
    args = parser.parse_args()
    
    api_key = os.getenv("NEXUS_API_KEY", "YOUR_API_KEY")  # Use environment variable for API key
    game_domain_name = args.game_domain_name
    csv_file = "extracted_data_with_id.csv"  # Default CSV file name
    category_reference_file = f"{game_domain_name}_categories_reference.csv"  # Default category file name

    # Check if category reference file exists, and create it if not
    if not os.path.exists(category_reference_file):
        print(f"Category reference file {category_reference_file} does not exist. Creating it...")
        game_info = get_game_info(game_domain_name, api_key)
        if game_info:
            create_category_reference_table(game_info.get("categories", []), category_reference_file)
        else:
            print("Failed to retrieve game information. Cannot create category reference file.")
            return

    # Process the CSV file for mod references
    process_mods_from_csv(csv_file, api_key, game_domain_name, category_reference_file)

if __name__ == "__main__":
    main()
