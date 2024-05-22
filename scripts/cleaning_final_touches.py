import extract_output
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
    api = extract_output.extract_api_output(line)
    formatted_output = "\n".join([f"{key}: {value}" for key, value in api.items()])

    inst = remove_backslashes(str(extract_output.extract_inst_text(line)))

    seed_modified_outputs = "<s>[INST]"+ inst +" [/INST]"+ str(api).strip('{}') +" </s>"

    with open('data/seed_modified_clean_outputs2.jsonl', 'a', encoding="utf-8") as fw:
        fw.write(json.dumps(seed_modified_outputs, ensure_ascii=False) + '\n')
        fw.close() 
