# -*- coding: utf-8 -*-
"""infrence_zero_shot_and_retrival.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17lKMS7nBRlEczRlpduDbM0_BgfKD1yqq
"""


from huggingface_hub import login
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

# Log in to Hugging Face
login(token="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")

# Configuration for 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

# Load the base model
base_model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    quantization_config=bnb_config,
    device_map="cuda",
    trust_remote_code=True,
)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_id, add_bos_token=True, trust_remote_code=True)

# Load the fine-tuned model
from peft import PeftModel
ft_model = PeftModel.from_pretrained(
    base_model,
    "/content/Llama-3-8B-Instruct-aragorilla"
)

# Ensure that the fine-tuned model and its components are moved to GPU
ft_model.to('cuda')

# Initialize the pipeline with the fine-tuned model
pipe = pipeline(
    task="text-generation",
    model=ft_model,
    tokenizer=tokenizer,
    max_length=1500,
     # Ensure the pipeline is set to use the GPU
)



def format_and_print(text):
    # Example: Split by comma and format each line
    lines = text.split(", '")
    if lines[0].startswith("<s>[INST]"):
        print(lines[0])
        lines = lines[1:]

    for line in lines:
        print(f"'{line.strip()}")


# Function to encode the question
def encode_question(question):
    domains = (
        "1. $DOMAIN should include one of {Multimodal Feature Extraction, Multimodal Text-to-Image, Multimodal Image-to-Text, Multimodal Text-to-Video, "
        "Multimodal Visual Question Answering, Multimodal Document Question Answer, Multimodal Graph Machine Learning, Computer Vision Depth Estimation, "
        "Computer Vision Image Classification, Computer Vision Object Detection, Computer Vision Image Segmentation, Computer Vision Image-to-Image, "
        "Computer Vision Unconditional Image Generation, Computer Vision Video Classification, Computer Vision Zero-Shot Image Classification, "
        "Natural Language Processing Text Classification, Natural Language Processing Token Classification, Natural Language Processing Table Question Answering, "
        "Natural Language Processing Question Answering, Natural Language Processing Zero-Shot Classification, Natural Language Processing Translation, "
        "Natural Language Processing Summarization, Natural Language Processing Conversational, Natural Language Processing Text Generation, Natural Language Processing Fill-Mask, "
        "Natural Language Processing Text2Text Generation, Natural Language Processing Sentence Similarity, Audio Text-to-Speech, Audio Automatic Speech Recognition, "
        "Audio Audio-to-Audio, Audio Audio Classification, Audio Voice Activity Detection, Tabular Tabular Classification, Tabular Tabular Regression, "
        "Reinforcement Learning Reinforcement Learning, Reinforcement Learning Robotics }"
    )

    prompt = (
        question + "\nWrite a python program in 1 to 2 lines to call API in huggingface. \n\n"
        "The answer should follow the format: <<<domain>>> $DOMAIN, <<<api_call>>>: $API_CALL, <<<api_provider>>>: $API_PROVIDER, <<<explanation>>>: $EXPLANATION, <<<code>>>: $CODE}. "
        "Here are the requirements:\n" + domains + "\n2. The $API_CALL should have only 1 line of code that calls api.\n"
        "3. The $API_PROVIDER should be the programming framework used.\n4. $EXPLANATION should be a step-by-step explanation.\n"
        "5. The $CODE is the python code.\n6. Do not repeat the format in your answer."
    )
    prompts = [
        {"role": "system", "content": "You are a helpful API writer who can write APIs based on requirements."},
        {"role": "user", "content": prompt}
    ]
    return prompt

from langchain_community.retrievers import BM25Retriever
import json
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import re

def extract_api(text):
    match = re.search(r'\\n###Output: (.*)', text)

    # If a match is found, extract the matched text
    if match:
        return match.group(1).strip()
    else:
        return "No match found."

def retriverBM25(query, doc_path):
  with open(doc_path, 'r') as f:
      data = [line for line in f]

  docs = [Document(page_content=json.dumps(item, ensure_ascii= False)) for item in data]

  texts = [doc.page_content for doc in docs]

  tokenized_texts = [text.split() for text in texts]

  bm25 = BM25Okapi(tokenized_texts)

  tokenized_query = query.split()

  top_n = 5
  top_docs_indices = bm25.get_top_n(tokenized_query, range(len(tokenized_texts)), n=top_n)
  retriever_result = [docs[i].page_content for i in top_docs_indices]

  # for idx, result in enumerate(retriever_result):
      # print(f"Result {idx+1}: {result}\n")


  # Incorporate the result into a prompt for Ara-Gorilla
  retriever_result_content = "".join(retriever_result[0])
  retriever_result_content = extract_api(retriever_result_content)

  question =  query + "Use this Reference API: " + retriever_result_content
  return question

"""# Eval instructions:"""

def extract_inst_text(text):
    # Define the regex pattern to match text between <s>[INST] and [/INST]
    pattern = re.compile(r'<s>\[INST\](.*?)\[/INST\]', re.DOTALL)

    # Find the first match
    match = pattern.search(text)

    if match:
        return match.group(1).strip()
    return None

with open('/content/aragorilla_eval.jsonl', 'r') as f:
    inst_eval_data = [extract_inst_text(line) for line in f]

with open('/content/inst_aragorilla_eval.jsonl', 'w') as f:
    f.write('\n'.join(inst_eval_data))

"""Eval Instructions:"""

with open('//content/inst_aragorilla_eval.jsonl', 'r') as f:
    inst_eval_data = [str(line).strip('\"') for line in f]

ten_inst= inst_eval_data[:21]
for i in range(len(ten_inst)):
  #print in enumrate
  print(i, ten_inst[i])

  print()

"""# Zero-Shot Infrence:"""

i=0

for query in inst_eval_data[:21]:
  # Perform inference
  result = pipe(f"<s>[INST] {encode_question(query)} [/INST]")
  generated = result[0]['generated_text']
  print(generated)

  print(i)
  i+=1

    # print(result[0]['generated_text'])
    # print(format_and_print(generated))

    # Write the extracted texts to a new JSONL file
  with open('/content/Zero_Shot_Infrence_results.jsonl', 'a') as f:
    f.write(json.dumps(generated, ensure_ascii=False) + '\n')

"""# Retrival Infrence:"""

i=0

for prompt in inst_eval_data[11:21]:

  query = retriverBM25(prompt, "/content/translated_api.jsonl")

  # Perform inference
  result = pipe(f"<s>[INST] {encode_question(query)} [/INST]")
  generated = result[0]['generated_text']
  print(generated)

  print(i)
  i+=1

  # Write the extracted texts to a new JSONL file
  with open('/content/Retrival_Infrence_results.jsonl', 'a') as f:
    f.write(json.dumps(generated, ensure_ascii=False) + '\n')
