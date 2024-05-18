import json
from openai import openai
import numpy as np
from rouge_score import rouge_scorer
import random

# Create the OpenAI client with the API key
client = OpenAI(
    api_key="sk-proj-znIW3TPZgXFdEt1ag9dxT3BlbkFJv2rdM6CGzdEwG6qhJQzP",
)

def load_seed_tasks(seed_tasks_path):
    """Load seed tasks from the specified JSONL file."""
    with open(seed_tasks_path, encoding="utf-8") as f:
        seed_tasks = [json.loads(line) for line in f]
    return seed_tasks

def load_api_entries(api_file):
    """Load API entries from the specified JSONL file."""
    with open(api_file, "r", encoding="utf-8") as f:
        api_entries = [json.loads(line.strip()) for line in f]
    return api_entries


def sample_from_seed(seed_tasks, num_samples):
    """Sample from the seed tasks."""
    return random.sample(seed_tasks, min(num_samples, len(seed_tasks)))


# genearte

api_file = "data\huggingface_api.jsonl"
seed_tasks_path = "seed_6.jsonl"

samples_api_file = "samples_api_file.jsonl"


seed_entries = load_seed_tasks(seed_tasks_path)
api_entries = load_api_entries(api_file)

gpt_instructions = []

for api_entry in api_entries[5]:

    sampled_seed_instructions = sample_from_seed(seed_entries, 3)

    user_message_content =("""
    using these 3 (instructon-instance) pairs for the given API with this format: 
    {"domain": "", "framework": "", "functionality": "", "api_name": "", "api_call": "", "api_arguments": "", "python_environment_requirements": "", "example_code": "", "performance": {"dataset": "", "accuracy": ""}, "description": ""} 
    Generate example (instructon-instance) pairs and make sure the instructions and exeplination in Arabic also make the results in the same format
    note: (don't use the API name when generate instrutions)""")
    
    data_to_write = [sampled_seed_instructions,api_entry]
    
    prompts = [user_message_content,data_to_write]
    
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system","content": "You are exampels generator"},
          {"role": "user", "content": str(prompts) },
      ],
  )
    
    
    for choice in completion.choices[:10]:
        
        gpt_instructions = choice.message.content
        with open('generated.jsonl', 'a', encoding="utf-8") as ft:
            ft.write(json.dumps(gpt_instructions,ensure_ascii=False) + '\n')
            ft.close()
            
            
            print(gpt_instructions, sep="\n")


# # user_message_content += data_to_write

# print(user_message_content)
# print("----------------------------------------------------------")

# with open("generate_file.json", "a", encoding="utf-8") as f:
#     f.write(json.dumps(user_message_content, ensure_ascii=False) + "\n")
#     f.write(json.dumps(data_to_write, ensure_ascii=False) + "\n")


# def save_sampled_instructions(sampled_instructions, output_file):
#     """Save sampled instructions to a JSONL file."""
#     with open(output_file,"w", encoding="utf-8") as f:
#         for instruction in sampled_instructions:
#             f.write(json.dumps(instruction,ensure_ascii=False) + "\n")