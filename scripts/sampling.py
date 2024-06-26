import json
import random

def load(file_path):
    """Load from the specified JSONL file."""
    with open(file_path, encoding="utf-8") as f:
        seed_tasks = [json.loads(line) for line in f]
    return seed_tasks


def sample_from_seed(seed_tasks, num_samples):
    """Sample from the seed tasks."""
    return random.sample(seed_tasks, min(num_samples, len(seed_tasks)))



if __name__ == "__main__":

    seed_tasks_path = "data\seed.jsonl"
    seed_tasks = load(seed_tasks_path)
    
    
    api_entries_path = 'data\huggingface_api.jsonl'
    api_entries = load(api_entries_path)


    print(f"Loaded {len(seed_tasks)} human-written seed instructions")
    
        
    with open('inst_api_pairs.jsonl', "w", encoding="utf-8") as f:
        for api_entry in api_entries:
            sampled_seed_instructions = sample_from_seed(seed_tasks, 3)

            for instruction in sampled_seed_instructions:
                
                inst_api_pairs = {'data':instruction,'api':api_entry}
                f.write(json.dumps(inst_api_pairs, ensure_ascii=False) + "\n")
            
            # print(inst_api_pairs)