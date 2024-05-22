import re
import json

def remove_backslashes(text):
    # Regular expression to match sequences of 3 or more backslashes

    pattern = r'\\{3,}'
    
    # Remove sequences of 3 or more backslashes followed by a double quote
    result = re.sub(pattern, '', text)
    
    # Remove any remaining double quotes
    result = result.replace('"', '')
    result = result.replace('\\', '')

    
    return result


with open("data/llama_format.jsonl", encoding="utf-8") as f:
    outputs = [line for line in f]

for line in outputs:
    inst = remove_backslashes(line)
    with open('data/seed_modified_no_slashes.jsonl', 'a', encoding="utf-8") as fw:
        fw.write(json.dumps(inst, ensure_ascii=False) + '\n')
        fw.close()