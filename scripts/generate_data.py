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


# genearte

for api_entry in api_entries:
    
    sampled_seed_instructions = random.sample(seed_task, 3)
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
        
        with open('data\generated.jsonl', 'a', encoding="utf-8") as ft:
            ft.write(json.dumps(gpt_instructions,ensure_ascii=False) + '\n')
            ft.close()
            
            # print(gpt_instructions, sep="\n")

        
        


        
        
            
   
    




