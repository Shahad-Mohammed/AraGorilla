import json
import random


def load_seed_tasks(seed_tasks_path):
    """Load seed tasks from the specified JSONL file."""
    with open(seed_tasks_path, encoding="utf-8") as f:
        seed_tasks = [json.loads(line) for line in f]
    return seed_tasks

def sample_from_seed(seed_tasks, num_samples):
    """Sample from the seed tasks."""
    return random.sample(seed_tasks, min(num_samples, len(seed_tasks)))

def save_sampled_instructions(sampled_instructions, output_file):
    """Save sampled instructions to a JSONL file."""
    with open(output_file,"w", encoding="utf-8") as f:
        for instruction in sampled_instructions:
            f.write(json.dumps(instruction,ensure_ascii=False) + "\n")

# if __name__ == "__main__":

#     seed_tasks_path = "seed_6.jsonl"
#     seed_tasks = load_seed_tasks(seed_tasks_path)

#     # seed_instructions = [t["instruction"] for t in seed_tasks]
#     # seed_instructions = seed_tasks
#     print(f"Loaded {len(seed_tasks)} human-written seed instructions")
    
#     # Sample instructions from the seed file
#     num_prompt_instructions = 3  
#     sampled_seed_instructions = sample_from_seed(seed_tasks, num_prompt_instructions)

#     print("Sampled instructions from the seed file:")
#     for instruction in sampled_seed_instructions:
#         print(instruction)


# # to save the samples only 

#     output_file = "sampled_instructions.jsonl"

#     save_sampled_instructions(sampled_seed_instructions, output_file)
#     print(f"Sampled instructions saved to {output_file}")
