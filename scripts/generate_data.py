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

def sample_from_seed(seed_tasks, num_samples):
    """Sample from the seed tasks."""
    return random.sample(seed_tasks, min(num_samples, len(seed_tasks)))



seed_file_path = "data\seed.jsonl"
seed_task = load(seed_file_path)


api_file_path = "data\huggingface_api.jsonl"
api_entries = load(api_file_path)


inst_api_path = "data\inst_api_pairs.jsonl"
inst_api_pairs = load(inst_api_path)



# Open the JSONL file
with open('data\inst_api_pairs.jsonl', 'r', encoding='utf-8') as f:
    # Read each line and parse it as JSON
    for line in f:
        # Parse the JSON from the current line
        data = json.loads(line.strip())
        
        # Access the fields as needed
        instruction = data['data']['instruction']
        # print(instruction)
        with open('inst_test.jsonl', "a", encoding="utf-8") as f:
            f.write(json.dumps(instruction, ensure_ascii=False) + "\n")



# genearte

for api_entry in api_entries[130:]:
    
    sampled_seed_instructions = sample_from_seed(seed_task, 3)
    user_message_content =("Generate 10 new (instruction-api pairs) and use the api provided as reference\n")
    api_entry = {"api":api_entry}
    
    
    
    inst_api_pairs=[]

    for instraction in sampled_seed_instructions:
        
        # print(instraction,api_entry)
        inst_api_pairs.append([instraction,api_entry])
        
    
    # print(user_message_content, str(inst_api_pairs))
    
    
    
    
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system","content": "You are an expert in API and instruction generation."},
          {"role": "user", "content": (user_message_content +" "+str(inst_api_pairs)) },
      ],
  )
    
    
    
    for choice in completion.choices[:10]:
        gpt_instructions = choice.message.content
        
        with open('generated.jsonl', 'a', encoding="utf-8") as ft:
            ft.write(json.dumps(gpt_instructions,ensure_ascii=False) + '\n')
            ft.close()
            
            # print(gpt_instructions, sep="\n")

        
        


        
        
            
   
    




