import json
from openai import OpenAI
import numpy as np
from rouge_score import rouge_scorer
import random

# Create the OpenAI client with the API key
client = OpenAI(
    api_key="sk-proj-znIW3TPZgXFdEt1ag9dxT3BlbkFJv2rdM6CGzdEwG6qhJQzP",
)


def load(file_path):
    """Load from the specified JSONL file."""
    with open(file_path, encoding="utf-8") as f:
        seed_tasks = [json.loads(line) for line in f]
    return seed_tasks


seed_file_path = "data\seed.jsonl"
seed_task = load(seed_file_path)

api_file_path = "data\huggingface_api.jsonl"
api_entries = load(api_file_path)


# Generate
for api_entry in api_entries[0:1]:
    sampled_seed_instructions = random.sample(seed_task, 3)
    
    inst_api_pairs = []
    for instruction in sampled_seed_instructions:
        inst_api_pairs.append({"instruction": instruction, "api": api_entry})

    user_message_content = "Generate 10 new (instruction-api pairs) and use the api provided as reference\n"
    for pair in inst_api_pairs:
        instruction = pair["instruction"]["instruction"]
        user_message_content += (
            f"""
            {{
                "instruction": "{instruction}",
                "api": {{
                    "domain": "{pair['api']['domain']}",
                    "framework": "{pair['api']['framework']}",
                    "functionality": "{pair['api']['functionality']}",
                    "api_name": "{pair['api']['api_name']}",
                    "api_call": "{pair['api']['api_call']}",
                    "api_arguments": "{pair['api']['api_arguments']}",
                    "python_environment_requirements": "{pair['api']['python_environment_requirements']}",
                    "example_code": "{pair['api']['example_code']}",
                    "performance": {{
                        "dataset": "{pair['api']['performance']['dataset']}",
                        "accuracy": "{pair['api']['performance']['accuracy']}"
                    }},
                    "description": "{pair['api']['description']}"
                }}
            }},
            """
        )
        
    # print(user_message_content)

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
            ft.write(json.dumps(gpt_instructions, ensure_ascii=False) + '\n')
    
    # print(gpt_instructions)
            
    
            
            
            

