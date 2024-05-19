import re 
import json
from langdetect import detect
from mtranslate import translate
from rouge_score import rouge_scorer

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

####Function to Check all required components are exsist
def check_required_components(input_string):
    Complete_instructions = []

    # List of required components
    required_components = [
        'instruction', 'api', 'domain', 'framework', 'functionality', 
        'api_name', 'api_call', 'api_arguments', 'python_environment_requirements', 
        'example_code', 'performance', 'description'
    ]
    missing_components = [component for component in required_components if component not in input_string]
    if not(missing_components):
      Complete_instructions.append(input_string)

    return Complete_instructions



#Filltering Arabic instructions:


#Open Generateion (before filltering) file:
with open('data/pool2.jsonl') as f:
###Open Generateion (before filltering) file:

 with open('/content/generated.jsonl') as f:
    gpt_instructions_before_filltering = [json.loads(line) for line in f]

# Function to translate
def translate_en_to_ar(text):
    translated_text = translate(text, 'ar', 'auto')
    return translated_text

# Function to extract and translate instructions
def extract_instructions_and_translate_it(inst):
      # Define regex patterns to match instructions
  pattern1 = re.compile(r'Instruction:\s*(.*?)\n\s*API:', re.DOTALL)
  pattern2 = re.compile(r"'instruction':\s*'(.*?)'", re.DOTALL)
      
      # Find all matches for each pattern
  instructions1 = pattern1.findall(inst)
  instructions2 = pattern2.findall(inst)

      # Print all instructions
  instruction = instructions1 + instructions2
  instruction_content = str(instruction).strip("[]")

  arabic_sure_instruction = ""

  if instruction_content:
    if detect(instruction_content) != 'ar':
      arabic_sure_instruction = inst.replace(instruction_content, translate_en_to_ar(instruction_content))
    else:
      arabic_sure_instruction = inst
  else:
    # Handle the case where instruction_content is empty
    # For example, you could raise an exception or return a default value
    pass

  return arabic_sure_instruction


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

#Complete Instructions
Complete_instructions = []
for ins in (gpt_instructions_before_filltering[:8]):
      if(check_required_components(ins)):
        Complete_instructions.append(ins)


gpt_instructions_vaild_notdublicated = filter_invalid_instances(filter_duplicate_instances(Complete_instructions))

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

#similarty code

# sampled_seed_instructions = random.sample(seed_task, 3)
# sentences = [item['instruction'] for item in sampled_seed_instructions]
# for sentence in sentences:
#     print(sentence)
#     similarity(sentences,sentence) 