import json

# Function to read JSON data from a file
def read_json_from_file(file_path):
    with open('/root/ha/atlas/code-py/all_types.json', 'r') as file:
        data = json.load(file)
    return data

# Function to pretty print JSON object
def pretty_print_json(obj):
    print(json.dumps(obj, indent=2))

# Replace 'data.json' with the path to your JSON file
file_path = 'data.json'

# Read JSON data from the file
data = read_json_from_file(file_path)

# Filter objects that contain "s3" in the "name" property
objects_with_s3 = [obj for obj in data if "s3_v2" in obj["name"].lower()]

# Print the JSON objects containing "s3" in their "name" property
for obj in objects_with_s3:
    pretty_print_json(obj)