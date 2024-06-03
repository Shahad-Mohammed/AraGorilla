# from transformers import AutoModelForSequenceClassification, AutoTokenizer

# model = AutoModelForSequenceClassification.from_pretrained("/home/ubuntu/aragorilla/AraGorilla/Llama-3-8B-Instruct-aragorilla/content/Llama-3-8B-Instruct-aragorilla")
# tokenizer = AutoTokenizer.from_pretrained("/home/ubuntu/aragorilla/AraGorilla/Llama-3-8B-Instruct-aragorilla/content/Llama-3-8B-Instruct-aragorilla")

# model.push_to_hub("Llama-3-8B-Instruct-aragorilla")
# tokenizer.push_to_hub("Llama-3-8B-Instruct-aragorilla")


# !pip install transformers==4.32.0
# !pip install sentencepiece
# !pip3 install auto-gptq==0.4.2
# !git clone https://huggingface.co/FreedomIntelligence/AceGPT-7b-chat-GPTQ

from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

model_id = 'AceGPT-7b-chat-GPTQ'
model = AutoGPTQForCausalLM.from_quantized(model_id,use_safetensors=False)
tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side="right", use_fast=False)


prompt_dict = {
    'AceGPT': """[INST] <<SYS>>\nأنت مساعد مفيد ومحترم وصادق.
    أجب دائما بأكبر قدر ممكن من المساعدة بينما تكون آمنا.
     يجب ألا تتضمن إجاباتك أي محتوى ضار أو غير أخلاقي أو عنصري أو جنسي أو سام أو خطير أو غير قانوني.
     يرجى التأكد من أن ردودك غير متحيزة اجتماعيا وإيجابية بطبيعتها.
     \n\nإذا كان السؤال لا معنى له أو لم يكن متماسكا من الناحية الواقعية،
      اشرح السبب بدلا من الإجابة على شيء غير صحيح. إذا كنت لا تعرف إجابة سؤال ما، فيرجى عدم مشاركة معلومات خاطئة.
      \n<</SYS>>\n\n""",
}

role_dict = {
    'AceGPT':['[INST]','[/INST]'],
}


def format_message(query, max_src_len):
    return f"""{prompt_dict["AceGPT"]}{query} {role_dict["AceGPT"][1]}"""


temperature=0.5
max_new_tokens = 768
content_len = 2048
message = 'نقوم بإنشاء تطبيق لتحويل الكلام إلى نص لمساعدة مستخدمينا في تسجيل الاجتماعات وتحويلها الى مذكرات نصية بشكل سريع وفعال؟'
history = []
max_src_len = content_len-max_new_tokens-8
prompt = format_message(message, max_src_len)

model_inputs  = tokenizer(prompt, return_tensors="pt").to("cuda")
output = model.generate(**model_inputs)
output.shape
tokenizer.decode(output[0])