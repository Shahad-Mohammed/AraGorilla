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


#Filltering Incomplete instances:

#Filltering Arabic instructions:
#Open Generateion (before filltering) file:
with open('/content/generated.jsonl') as f:
    gpt_instructions_before_filltering = [json.loads(line) for line in f]

# Function to extract and print instructions
def extract_instructions(text):
    instructions = []

    # Define regex patterns to match instructions
    pattern1 = re.compile(r'Instruction:\s*(.*?)\n\s*API:', re.DOTALL)
    pattern2 = re.compile(r"'instruction':\s*'(.*?)'", re.DOTALL)
    
    # Find all matches for each pattern
    instructions1 = pattern1.findall(text)
    instructions2 = pattern2.findall(text)
    
    # Print all instructions
    for instruction in instructions1 + instructions2:
      instructions.append(instruction.strip())
    return instructions

#Function to Transelate en to ar:
def translate_arabic_to_english(text):
    translated_text = translate(text, 'ar', 'auto')
    return translated_text


for i in range(len(gpt_instructions_before_filltering[:2])):
  instrs = extract_instructions(str(gpt_instructions_before_filltering[i]))
  for ins in instrs:
    if detect(ins) != 'ar':
      res = translate_arabic_to_english(ins)
      print(res)
      print()



########################################################################################################################
#                                                                                                                      #
#                                                                                                                      #
#                                          FILLTERING IMPLEMETION                                                      #
#                                                                                                                      #
#                                                                                                                      #
########################################################################################################################


gpt_instructions_vaild_notdublicated = filter_invalid_instances(filter_duplicate_instances(gpt_instructions))

scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

for i in gpt_instructions_vaild_notdublicated:
  i_score = scorer.score(str_store, i)
  if ( i_score < 0.7 for i in gpt_instructions):
   # Check if instruction is in Arabic Language
   # Check if instruction is complete
    # Appending the generated inst
    with open('generated_Insts.jsonl', 'a', encoding="utf-8") as f:
        f.write(json.dumps(i) + '\n')
        f.close()