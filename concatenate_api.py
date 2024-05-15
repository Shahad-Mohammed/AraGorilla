import json
import sampling 


def load_api_entries(api_file):
    """Load API entries from the specified JSONL file."""
    with open(api_file, "r", encoding="utf-8") as f:
        api_entries = [json.loads(line.strip()) for line in f]
    return api_entries


def save_api_entries_with_samples(data_to_write, samples_api_file):
    """Append API entries along with sampled instruction-instance pairs to a new JSONL file."""

    with open(samples_api_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(data_to_write, ensure_ascii=False) + "\n")


if __name__ == "__main__":

    api_file = "data\huggingface_api_2.jsonl"
    seed_tasks_path = "seed_6.jsonl"

    samples_api_file = "samples_api_file.jsonl"


    seed_entries = sampling.load_seed_tasks(seed_tasks_path)
    api_entries = load_api_entries(api_file)



    for api_entry in api_entries:
        sampled_seed_instructions = sampling.sample_from_seed(seed_entries, 3)
        data_to_write = [sampled_seed_instructions,api_entry]        
        
        with open(samples_api_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(data_to_write, ensure_ascii=False) + "\n")

   

