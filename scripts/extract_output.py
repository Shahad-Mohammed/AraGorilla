import re
import json

def extract_inst_text(text):
    # Define the regex pattern to match text between [INST] and [/INST]
    pattern = re.compile(r'\[INST\](.*?)?\[\/INST\]', re.DOTALL)
    
    # Find all matches
    matches = pattern.findall(text)
    
    return matches

def extract_api_output(text):
    # Define regex patterns for each field
    patterns = {
        'domain': r"'domain': '([^']+)'",
        'framework': r"'framework': '([^']+)'",
        'functionality': r"'functionality': '([^']+)'",
        'api_name': r"'api_name': '([^']+)'",
        'api_call': r"'api_call':\"([^\"]+)\"",
        'description': r"'description': '([^']+)'"
    }

    # Dictionary to store extracted information
    extracted_info = {}

    # Extract information using regex
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_info[key] = match.group(1)
        else:
            extracted_info[key] = None  # If no match is found, set as None

    return extracted_info

with open("data/llama_format.jsonl", encoding="utf-8") as f:
    outputs = [line for line in f]
    

# Extract api, inst
for line in outputs:
    api = extract_api_output(line)
    formatted_output = "\n".join([f"{key}: {value}" for key, value in api.items()])

    inst = str(extract_inst_text(line)).strip('[]'). replace('\\n','')

    seed_modified_outputs = "<s>[INST]"+ inst +" [/INST]"+ str(api).strip('{}') +" </s>"

    with open('data/seed_modified_outputs.jsonl', 'a', encoding="utf-8") as fw:
        fw.write(json.dumps(seed_modified_outputs, ensure_ascii=False) + '\n')
        fw.close() 