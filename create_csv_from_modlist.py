import json
import csv

# Define the input JSON file name
input_file_name = "modlist"

# Load the JSON data from a file
with open(input_file_name, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# List to store the extracted data
extracted_data = []

# Extract the relevant fields
for entry in json_data["Archives"]:
    name = entry.get("Name")
    description = entry.get("State", {}).get("Description")
    mod_id = entry.get("State", {}).get("ModID")
    
    # Append the extracted data to the list
    extracted_data.append({"Name": name, "Description": description, "modID": mod_id})

# Define the CSV file name
csv_file_name = "extracted_data_with_id.csv"

# Write the data to a CSV file
with open(csv_file_name, mode="w", newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["Name", "Description", "modID"])
    writer.writeheader()
    writer.writerows(extracted_data)

print(f"Data successfully written to {csv_file_name}")
