import json

with open('llama_format.jsonl', 'r', encoding="utf-8") as infile, open('data\llama_format.jsonl', 'w', encoding="utf-8") as outfile:
    for line in infile:
        json_object = {"text": line.strip("\"")}
        json_line = json.dumps(json_object, ensure_ascii=False)
        outfile.write(json_line+'\n')