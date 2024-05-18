import json
import re

def extract_apis(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # Regular expression to match the 'api' dictionaries
    api_pattern = re.compile(r"'api': ({.*?}\\n)", re.DOTALL)
    api_matches = api_pattern.findall(data)
    
    # Convert the extracted 'api' sections from strings to dictionaries
    #apis = [json.loads(api.replace("'", '"')) for api in api_matches]
    
    return api_matches

# Example usage
file_path = 'input.txt'
apis = extract_apis(file_path)
for i, api in enumerate(apis, start=1):
    print(f"API {i}:\n{json.dumps(api, indent=4)}\n")
