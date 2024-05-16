import json
from openai import OpenAI
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

# Load lines from another file
def load_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return lines


# genearte


api_file = "data\huggingface_api.jsonl"
api_entries = load_api_entries(api_file)


inst_api_path = "data\inst_api_pairs.jsonl"
inst_api_pairs = load_seed_tasks(inst_api_path)




lines = load_lines('data\inst_api_pairs.jsonl')


print(lines)



# # Combine each set of three lines with an API entry
# combined_data = []
# for i in range(0, len(api_entries), 937):
#     for j in range(i, min(i + 937, len(api_entries))):
#         combined_entry = {
#             "api": api_entries[j],
#             "lines": [lines[i], lines[i+1], lines[i+2]]
#         }
#         combined_data.append(combined_entry)


# # Write combined data to a new JSONL file
# with open('test_prompt.jsonl', "w", encoding="utf-8") as f:
#     for entry in combined_data:
#         f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# print("Combined data written to test_prompt.jsonl")




# for api_entry in api_entries[0:1]:
    
#     user_message_content =("""
#                            Generate 10 (instruction-api pairs) and use the api as reference from these data 
#                            """)
    
#     for data in inst_api_pairs:
#         # print(data,api_entry)
#         a  = [data,api_entry]
        
        
#         with open('test_prompt.jsonl', 'w', encoding="utf-8") as ft:
#             ft.write(json.dumps(a,ensure_ascii=False) + '\n')
        
        
          
#     prompts = [user_message_content,data_to_write]
    
#     completion = client.chat.completions.create(
#       model="gpt-3.5-turbo",
#       messages=[
#           {"role": "system","content": "You are exampels generator"},
#           {"role": "user", "content": str(prompts) },
#       ],
#   )
    
    
#     for choice in completion.choices[:10]:
        
#         gpt_instructions = choice.message.content
#         with open('generated.jsonl', 'a', encoding="utf-8") as ft:
#             ft.write(json.dumps(gpt_instructions,ensure_ascii=False) + '\n')
#             ft.close()
            
            
#             print(gpt_instructions, sep="\n")



    





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



