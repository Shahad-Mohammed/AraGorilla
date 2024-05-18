import re 
import json
from langdetect import detect
from mtranslate import translate



#Filltering Methods Duplication, Invalid:

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