from huggingface_hub import login
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from langchain_community.retrievers import BM25Retriever
import json

# Log in to Hugging Face
login(token="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")

# Configuration for 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

#
with open('/home/ubuntu/aragorilla/AraGorilla/data/huggingface_api.jsonl', 'r') as f:
    data = [json.loads(line) for line in f]
str_data = str(data).strip('[]')
print(str_data)

#Retriver Configuration
from langchain_core.documents import Document

for i in range(len(data)):
  docs = [Document(page_content=str(data[i])) for doc in data]

retriever = BM25Retriever.from_documents(docs)

# Load the base model
base_model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    quantization_config=bnb_config,
    device_map="cuda:0",
    trust_remote_code=True,
)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_id, add_bos_token=True, trust_remote_code=True)

# Load the fine-tuned model
from peft import PeftModel
ft_model = PeftModel.from_pretrained(
    base_model,
    "/home/ubuntu/aragorilla/AraGorilla/Llama-3-8B-Instruct-aragorilla/content/Llama-3-8B-Instruct-aragorilla"
)

# Ensure that the fine-tuned model and its components are moved to GPU
ft_model.to('cuda')

# Initialize the pipeline with the fine-tuned model
pipe = pipeline(
    task="text-generation",
    model=ft_model,
    tokenizer=tokenizer,
    max_length=1000,
    device=0  # Ensure the pipeline is set to use the GPU
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
    return prompts

# Question to encode
user_question = "نقوم بإنشاء تطبيق لترجمة النصوص من اللغة الانجليزية الى الصينية"
retriever_result = retriever.invoke(user_question)
prompt = user_question + str(retriever_result)

# Perform inference
result = pipe(f"<s>[INST] {prompt} [/INST]")
generated = result[0]['generated_text']
# print(result[0]['generated_text'])
print(format_and_print(generated))