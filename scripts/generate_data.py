import json
from openai import OpenAI
import numpy as np
from rouge_score import rouge_scorer
import random

from langdetect import detect
from mtranslate import translate
from fillter import extract_instructions,translate_arabic_to_english

# Create the OpenAI client with the API key
client = OpenAI(
    api_key="sk-proj-znIW3TPZgXFdEt1ag9dxT3BlbkFJv2rdM6CGzdEwG6qhJQzP",
)


def load(file_path):
    """Load from the specified JSONL file."""
    with open(file_path, encoding="utf-8") as f:
        seed_tasks = [json.loads(line) for line in f]
    return seed_tasks


seed_file_path = r"data\seed.jsonl"
seed_task = load(seed_file_path)

api_file_path = r"data\huggingface_api.jsonl"
api_entries = load(api_file_path)


# Generate
for api_entry in api_entries[0:1]:
    sampled_seed_instructions = random.sample(seed_task, 3)
    
    inst_api_pairs = []
    for instruction in sampled_seed_instructions:
        inst_api_pairs.append({"instruction": instruction, "api": api_entry})

    user_message_content = "Generate 10 new (instruction-api pairs) and use the api provided as reference\n"
    for i, pair in enumerate(inst_api_pairs, 1):
        instruction = pair["instruction"]["instruction"]
        i = 0
        user_message_content += (
            f"""
            {i}. instruction: {instruction}api: domain: {pair['api']['domain']} framework: {pair['api']['framework']} functionality: {pair['api']['functionality']} api_name: {pair['api']['api_name']} api_call: {pair['api']['api_call']} api_arguments: {pair['api']['api_arguments']} python_environment_requirements: {pair['api']['python_environment_requirements']} example_code: {pair['api']['example_code']} performance: dataset: {pair['api']['performance']['dataset']} accuracy: {pair['api']['performance']['accuracy']} description: {pair['api']['description']}"""
        )
                
    # print(user_message_content)

    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are an expert in API and instruction generation."},
    #         {"role": "user", "content": user_message_content},
    #     ],
    # )

    # for choice in completion.choices:
    #     gpt_instructions = choice.message.content
    #     with open(r'data\pool2.jsonl', 'a', encoding="utf-8") as ft:
    #         ft.write(json.dumps(gpt_instructions, ensure_ascii=False) + '\n')
    #         ft.close()
            
            
        # with open('data/pool2.jsonl',encoding="utf-8") as f:
        #     gpt_instructions_before_filltering = [json.loads(line) for line in f] 
            
            
            # print(gpt_instructions)
   # print(gpt_instructions)
        
    test="1. Instruction: \"We need a tool to analyze sentiment in customer reviews for our e-commerce platform. Can you suggest an API for this?\"\n   API: \n   - Domain: Natural Language Processing Sentiment Analysis\n   - Framework: Hugging Face Transformers\n   - Functionality: Sentiment Analysis\n   - API Name: VaderSentiment/vader-large\n   - API Call: AutoModel.from_pretrained('VaderSentiment/vader-large')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A pre-trained VADER large model for sentiment analysis provided by VaderSentiment, based on the Hugging Face Transformers library.\n\n2. Instruction: \"Our research project involves identifying named entities in legal texts. Which API would you recommend for named entity recognition in Arabic text?\"\n   API: \n   - Domain: Natural Language Processing Named Entity Recognition\n   - Framework: Hugging Face Transformers\n   - Functionality: Named Entity Recognition\n   - API Name: GEO-K/arabic-ner\n   - API Call: AutoModel.from_pretrained('GEO-K/arabic-ner')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A pre-trained Arabic named entity recognition model provided by GEO-K, based on the Hugging Face Transformers library.\n\n3. Instruction: \"We are developing a virtual assistant that needs to understand and respond to user queries in various languages. Could you recommend an API for multilingual text classification?\"\n   API: \n   - Domain: Natural Language Processing Text Classification\n   - Framework: Hugging Face Transformers\n   - Functionality: Text Classification\n   - API Name: Multilingual-BERT/multi-classification\n   - API Call: AutoModel.from_pretrained('Multilingual-BERT/multi-classification')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A pre-trained multilingual text classification model provided by Multilingual-BERT, based on the Hugging Face Transformers library.\n\n4. Instruction: \"Our marketing team needs a tool to analyze social media posts for brand sentiment. Can you recommend an API for sentiment analysis on Twitter data?\"\n   API: \n   - Domain: Natural Language Processing Sentiment Analysis\n   - Framework: Hugging Face Transformers\n   - Functionality: Sentiment Analysis\n   - API Name: Twitter-Sentiment/twitter-sentiment\n   - API Call: AutoModel.from_pretrained('Twitter-Sentiment/twitter-sentiment')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A specialized pre-trained model for sentiment analysis on Twitter data provided by Twitter-Sentiment, based on the Hugging Face Transformers library.\n\n5. Instruction: \"We require a tool to summarize long research articles into concise points for easier understanding. Which API can be used for text summarization?\"\n   API: \n   - Domain: Natural Language Processing Text Summarization\n   - Framework: Hugging Face Transformers\n   - Functionality: Text Summarization\n   - API Name: Summarizer/longformer-large-4096\n   - API Call: AutoModel.from_pretrained('Summarizer/longformer-large-4096')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A pre-trained longformer-large model for text summarization provided by Summarizer, based on the Hugging Face Transformers library.\n\n6. Instruction: \"We are building a chatbot for a customer service platform. Which API should we use for intent classification of user queries?\"\n   API: \n   - Domain: Natural Language Processing Intent Classification\n   - Framework: Hugging Face Transformers\n   - Functionality: Intent Classification\n   - API Name: CHITCHAT-GPT/intent-classification\n   - API Call: AutoModel.from_pretrained('CHITCHAT-GPT/intent-classification')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A pre-trained intent classification model for chatbot queries provided by CHITCHAT-GPT, based on the Hugging Face Transformers library.\n\n7. Instruction: \"Our educational platform needs a tool to generate multiple-choice questions from text passages. Can you suggest an API for question generation?\"\n   API: \n   - Domain: Natural Language Processing Question Generation\n   - Framework: Hugging Face Transformers\n   - Functionality: Question Generation\n   - API Name: QGen/gpt2-large\n   - API Call: AutoModel.from_pretrained('QGen/gpt2-large')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A pre-trained gpt2-large model for question generation provided by QGen, based on the Hugging Face Transformers library.\n\n8. Instruction: \"We are working on a project that involves analyzing customer feedback to identify key features for product improvement. Which API is suitable for feature extraction from text data?\"\n   API: \n   - Domain: Natural Language Processing Feature Extraction\n   - Framework: Hugging Face Transformers\n   - Functionality: Feature Extraction\n   - API Name: FeatureBERT/feature-extraction\n   - API Call: AutoModel.from_pretrained('FeatureBERT/feature-extraction')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A specialized pre-trained model for feature extraction from text data provided by FeatureBERT, based on the Hugging Face Transformers library.\n\n9. Instruction: \"Our team is developing a tool to recognize emotion in text conversations. Can you recommend an API for emotion detection in textual data?\"\n   API: \n   - Domain: Natural Language Processing Emotion Detection\n   - Framework: Hugging Face Transformers\n   - Functionality: Emotion Detection\n   - API Name: EmoBERT/emotion-classification\n   - API Call: AutoModel.from_pretrained('EmoBERT/emotion-classification')\n   - API Arguments: N/A\n   - Python Environment Requirements: transformers\n   - Example Code: N/A\n   - Performance: \n     - Dataset: N/A\n     - Accuracy: N/A\n   - Description: A pre-trained emotion classification model provided by EmoBERT for detecting emotions in textual data, based on the Hugging Face Transformers library.\n\n10. Instruction: \"We need a tool to analyze technical documents and extract key information for indexing purposes. Which API would you recommend for information extraction from documents?\"\n    API: \n    - Domain: Natural Language Processing Information Extraction\n    - Framework: Hugging Face Transformers\n    - Functionality: Information Extraction\n    - API Name: InfoExtractron/doc-extractor\n    - API Call: AutoModel.from_pretrained('InfoExtractron/doc-extractor')\n    - API Arguments: N/A\n    - Python Environment Requirements: transformers\n    - Example Code: N/A\n    - Performance: \n      - Dataset: N/A\n      - Accuracy: N/A\n    - Description: A specialized pre-trained model for extracting key information from technical documents provided by InfoExtractron, based on the Hugging Face Transformers library."
    instrs = extract_instructions(test)
    print(instrs)
    trans=translate_arabic_to_english(str(instrs).strip('"') )
    print(trans)
                
        # for ins in instrs:
            
        #     if isinstance(ins, tuple):
        #         ins_text = ins[0]
        #     else:
        #         ins_text = ins.strip('"') 
            
        #     if detect(ins_text) == 'en':
        #         res = translate_arabic_to_english(ins_text).strip('"') 
        #         instruction = {"instruction": res}
        #     else:
        #         instruction = {"instruction": ins_text}
            
        #     print(instruction)
        #     with open('data/seed.jsonl', "a", encoding="utf-8") as f:
        #         json.dump(instruction, f, ensure_ascii=False)
        #         f.write("\n")
        
            
