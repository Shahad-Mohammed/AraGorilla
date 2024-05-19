import re 
import json
from langdetect import detect
from mtranslate import translate


# #Open Generateion (before filltering) file:
# with open('data/pool2.jsonl',encoding="utf-8") as f:
#     gpt_instructions_before_filltering = [json.loads(line) for line in f]
    
# Function to extract and print instructions
def extract_instructions(text):
    instructions = []

    # Define regex patterns to match instructions
    pattern1 = re.compile(r'Instruction:\s*(.*?)\n\s*API:', re.DOTALL)
    pattern2 = re.compile(r"'instruction':\s*'(.*?)'", re.DOTALL)
    pattern3 = re.compile(r'\d+\. instruction: (.+?)(?=api:|$)', re.DOTALL)


    
    # Find all matches for each pattern
    instructions1 = pattern1.findall(text)
    instructions2 = pattern2.findall(text)
    instructions3 = pattern3.findall(text)

    
    # Print all instructions
    for instruction in instructions1 + instructions2+instructions3:
      instructions.append(instruction.strip())
    return instructions


#Function to Transelate en to ar:
def translate_arabic_to_english(text):
    translated_text = translate(text, 'ar', 'auto')
    return translated_text


# for i in range(len(gpt_instructions_before_filltering)):
#     instrs = extract_instructions(str(gpt_instructions_before_filltering[i]))
#     for ins in instrs:
#         # Assuming ins is a tuple, extract the first element
#         if isinstance(ins, tuple):
#             ins_text = ins[0]
#         else:
#             ins_text = ins.strip('"') 
        
#         if detect(ins_text) == 'en':
#             res = translate_arabic_to_english(ins_text).strip('"') 
#             instruction = {"instruction": res}
#         else:
#             instruction = {"instruction": ins_text}
        
#     print(instruction)