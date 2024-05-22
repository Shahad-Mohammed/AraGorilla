import json

# Function to process each JSON object
def process_data(data):
    # Extracting information from the input data
    instruction_key = "###Instruction:"
    output_key = "###Output:"
    code_key = "<<<code>>>:"

    # Split data["code"] into lines and extract relevant parts
    lines = data["code"].split('\n')
    instruction = lines[0].replace(instruction_key, '').strip()
    output = lines[1:]

    # Helper function to extract value after a specific marker
    def extract_value(marker, lines):
        for line in lines:
            if marker in line:
                return line.split(marker)[1].strip()
        return None

    # Extracting domain, api_call, api_provider, explanation, and code
    domain = extract_value('<<<domain>>>: ', output)
    api_call = extract_value('<<<api_call>>>: ', output)
    api_provider = extract_value('<<<api_provider>>>: ', output)

    # Extracting explanation (lines starting with <<<explanation>>>)
    explanation_lines = [line.replace('<<<explanation>>>: ', '') for line in output if line.startswith('<<<explanation>>>: ')]
    explanation = ' '.join(explanation_lines)

    # Extracting code (lines starting with <<<code>>> and onwards until a new marker is found)
    code_start_index = None
    for idx, line in enumerate(output):
        if line.startswith('<<<code>>>: '):
            code_start_index = idx
            break

    code_lines = []
    if code_start_index is not None:
        for line in output[code_start_index:]:
            if line.startswith('<<<') and not line.startswith('<<<code>>>: '):
                break
            code_lines.append(line.replace('<<<code>>>: ', ''))

    code = '\n'.join(code_lines).strip()

    # Construct the final dictionary
    output_dict = {
        "domain": domain,
        "api_call": api_call,
        "api_provider": api_provider,
        "explanation": explanation,
        "code": code,
        "api_data": {
            **data["api_data"],
            "api_call": code  # Overwriting the api_call with the entire code content
        }
    }
    return output_dict

# Read the JSONL file line by line
with open("data/huggingface_train.jsonl", encoding="utf-8") as f:
    lines = f.readlines()

# Process each JSON object and write the output to a new JSONL file
with open('data2.jsonl', "w", encoding="utf-8") as f:
    for line in lines:
        data = json.loads(line)
        output_dict = process_data(data)
        output_json = json.dumps(output_dict, ensure_ascii=False)
        f.write(output_json + "\n")
