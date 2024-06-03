import json
import re
import jsonlines
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text):
    reshaped_text = reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

model_name = "aubmindlab/bert-base-arabertv2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def cosine_similarity_between_texts(text1, text2):
    text1_preprocessed = preprocess_text(text1)
    text2_preprocessed = preprocess_text(text2)

    embeddings1 = get_embeddings(text1_preprocessed)
    embeddings2 = get_embeddings(text2_preprocessed)

    similarity = cosine_similarity(embeddings1.detach().numpy(), embeddings2.detach().numpy())
    return similarity[0][0]

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)  # Average pooling
    return embeddings


def transform_structure(input_file): # extract instruction ,domain ,api_call from translated_api.jsonl (our dataset)
    api_dataset=[]
    with jsonlines.open(input_file) as reader:
        for obj in reader:
            # Extract necessary fields from the original JSON object
            code = obj.get("code", "")
            api_call = obj.get("api_call", "")
            api_data = obj.get("api_data", {})
            # Extract the domain
            domain = api_data.get('domain', '')
            instruction_match = re.search(r'###Instruction:(.*?)###Output:', code, re.DOTALL)
            instruction = instruction_match.group(1).strip() if instruction_match else ''

            # Construct the new structure
            new_structure = {"instruction: ":instruction ,'domain':domain,"api_call": api_call}




            # Write the new structure to the output file
            api_dataset.append(new_structure)
    return api_dataset


def transform_structure2(input_file): # extract instruction ,domain ,api_call from aragorilla_eval.jsonl (responses)
    responses = []
    with jsonlines.open(input_file) as reader:
        for obj in reader:
            # Extract necessary fields from the original JSON object
            text = obj.get("text", "")
            instruction_match = re.search(r'\[INST\](.*?)\[/INST\]', text, re.DOTALL)
            instruction = instruction_match.group(1).strip() if instruction_match else ''
            domain_patterns = [
                r"'domain':\s*'([^']*)'",
                r'<<<domain>>>\':\s*\'([^\']*)\'',
                r'<<<domain>>>\'\:\s*\'(.*?)\''

                ]

            domain_patterns2=[
                r'<<<api_call>>>\":\s*\\\\\"([^\"]*)\\\\\"',
                r'<<<api_call>>>\'\:\s*\\\"(.*?)\\\"',
                r"'api_call':\s*'([^']*)'",
                r"'api_call':\s*\\\\\"([^\"]*)\\\\\"",
                r'<<<api_call>>>\':\s*\\\\\"([^\"]*)\\\\\"'

                              ]

            domain =''
            for pattern in domain_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    domain = matches[0]
                    break

            api_call =''
            for pattern in domain_patterns2:
                matches = re.findall(pattern, text)
                if matches:
                    api_call = matches[0]
                    break

            # Construct the new structure
            null_value=0
            new_structure = {"instruction": instruction, 'domain': domain, "api_call": api_call}
            if api_call=='':
                null_value=+1

            # Write the new structure to the output file
            responses.append(new_structure)

    return responses



api_dataset=transform_structure(r"translated_api.jsonl")
responses=transform_structure2(r"aragorilla_eval.jsonl")


total_similarity = 0
count = 0

for response in responses:
    for api_data in api_dataset:
        if api_data['api_call'] == response['api_call']:
          similarity = cosine_similarity_between_texts(api_data['instruction: '], response['instruction'])
          if similarity > 0.5:
            total_similarity += similarity
            count += 1
            break

if count > 0:
    final_cosine_similarity = total_similarity / count
else:
    final_cosine_similarity = 0

print(f"Final Cosine Similarity: {final_cosine_similarity}")