import json
import random
from rouge_score import rouge_scorer

def filter_duplicate_instances(instances):
    # remove duplicate instances
    instances = list(set(instances))
    return instances

def filter_invalid_instances(instances):
    filtered_instances = []
    for instance in instances:
        # if input and output are the same, we will not use such instances
        if instance[1] == instance[2]:
            continue
        # if output is empty, we will not use such instances
        if instance[2] == "":
            continue
        # if input or output ends with a colon, these are usually imcomplete generation. We will not use such instances
        if instance[1].strip().endswith(":") or instance[2].strip().endswith(":"):
            continue
        filtered_instances.append(instance)
    return filtered_instances




def filterd(gpt_instructions, Pool):

    gpt_instructions_vaild_notdublicated = filter_invalid_instances(filter_duplicate_instances(gpt_instructions))
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

    for i in gpt_instructions_vaild_notdublicated:
        i_score = scorer.score(Pool, i)
        if ( i_score < 0.7 for i in gpt_instructions):
        # Appending the generated inst

            with open('generated_Insts.jsonl', 'a', encoding="utf-8") as f:
                f.write(json.dumps(i) + '\n')
                f.close()