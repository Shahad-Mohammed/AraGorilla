import json
from openai import OpenAI
import numpy as np
from rouge_score import rouge_scorer
import random

from langdetect import detect
from mtranslate import translate
from fillter import extract_instructions,translate_arabic_to_english,similarity

# Create the OpenAI client with the API key
client = OpenAI(
    api_key="sk-proj-znIW3TPZgXFdEt1ag9dxT3BlbkFJv2rdM6CGzdEwG6qhJQzP",
)


def load(file_path):
    """Load from the specified JSONL file."""
    with open(file_path, encoding="utf-8") as f:
        seed_tasks = [json.loads(line) for line in f]
    return seed_tasks


seed_file_path = "data\seed2.jsonl"
seed_task = load(seed_file_path)

api_file_path = "data\huggingface_api.jsonl"
api_entries = load(api_file_path)


#Generate
for api_entry in api_entries[209:]:
    random.shuffle(seed_task)
    sampled_seed_instructions = random.sample(seed_task, 3)

    inst_api_pairs = []
    for instruction in sampled_seed_instructions:
        inst_api_pairs.append({"instruction": instruction, "api": api_entry})

    user_message_content = "Generate 10 new (instruction-api pairs) and use the api provided as reference\n"
    for i, pair in enumerate(inst_api_pairs, 1):
        instruction = pair["instruction"]["instruction"]
        accuracy = pair['api']['performance'].get('accuracy', 'N/A')

        i = 0
        user_message_content += (
            f"""
            {i}. instruction: {instruction} api: domain: {pair['api']['domain']} framework: {pair['api']['framework']} functionality: {pair['api']['functionality']} api_name: {pair['api']['api_name']} api_call: {pair['api']['api_call']} api_arguments: {pair['api']['api_arguments']} python_environment_requirements: {pair['api']['python_environment_requirements']} example_code: {pair['api']['example_code']} performance: dataset: {pair['api']['performance']['dataset']} accuracy: {accuracy} description: {pair['api']['description']}"""
        )
                

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in API and instruction generation."},
            {"role": "user", "content": user_message_content},
        ],
    )

    for choice in completion.choices:
        gpt_instructions = choice.message.content
        with open('data\pool2.jsonl', 'a', encoding="utf-8") as ft:
            ft.write(json.dumps(gpt_instructions,ensure_ascii=False) + '\n')
            ft.close()
            
            
        with open('data/pool2.jsonl',encoding="utf-8") as f:
            gpt_instructions_before_filltering = [json.loads(line) for line in f] 
            
            
    instrs = extract_instructions(gpt_instructions)
    trans = translate_arabic_to_english((str(instrs).strip('"')).strip('[]') )

    for i in trans.split(',') :
        if i != "''":
            
            llama_format = "<s>[INST]"+ str(i.replace("'","")).strip("{}") +"? [/INST]"+ str(api_entry).strip("{{}}") +" </s>"
            with open('data/llama_format.jsonl', 'a', encoding="utf-8") as fw:
                fw.write(json.dumps(llama_format, ensure_ascii=False) + '\n')
                fw.close()  
                
                
                
            instruction = {"instruction": i.replace("'","")}
            with open('data/seed2.jsonl', 'a', encoding="utf-8") as fw:
                fw.write(json.dumps(instruction, ensure_ascii=False) + '\n')
                fw.close()
                
        else:
            None


    