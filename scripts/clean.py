
# import jsonlines

# def transform_structure(input_file, output_file):
#     with jsonlines.open(input_file) as reader, jsonlines.open(output_file, mode='w') as writer:
#         for obj in reader:
#             # Extract necessary fields from the original JSON object
#             code = obj.get("code", "")
#             api_call = obj.get("api_call", "")
#             provider = obj.get("provider", "")
#             api_data = obj.get("api_data", {})

#             # Extract the domain
#             domain = api_data.get('domain', '')

#             # Extract the explanation part
#             explanation_start = code.find("<<<explanation>>>:") + len("<<<explanation>>>:")
#             code_start = code.find("<<<code>>>:")
#             if explanation_start != -1 and code_start != -1:
#                 explanation = code[explanation_start:code_start].strip()
#             else:
#                 explanation = ""

#             # Extract the code part
#             if "<<<code>>>:" in code:
#                 code_part = code.split("<<<code>>>:")[1].strip()
#             else:
#                 code_part = ""

#             # Construct the new structure
#             new_structure = {
#                 "domain": domain,
#                 "api_call": api_call,
#                 "api_provider": provider,
#                 "explanation": explanation,
#                 "code": code_part,
#                 "api_data": {
#                     "domain": domain,
#                     "framework": "Hugging Face Transformers",
#                     "functionality": "Feature Extraction",
#                     "api_name": api_data.get('api_name', ''),
#                     "api_call": api_data.get('api_call', ''),
#                     "api_arguments": api_data.get('api_arguments', 'N/A'),
#                     "python_environment_requirements": api_data.get('python_environment_requirements', 'transformers'),
#                     "example_code": api_data.get('example_code', 'N/A'),
#                     "performance": api_data.get('performance', {"dataset": "N/A", "accuracy": "N/A"}),
#                     "description": api_data.get('description', 'A pre-trained ConvBERT model for feature extraction provided by YituTech, based on the Hugging Face Transformers library.')
#                 }
#             }

#             # Include the api_call and provider in the code part if necessary
#             if "api_call" not in new_structure["code"]:
#                 new_structure["code"] += f"\n# API Call: {api_call}"
#             if "provider" not in new_structure["code"]:
#                 new_structure["code"] += f"\n# Provider: {provider}"

#             # Write the new structure to the output file
#             writer.write(new_structure)

# # Specify the input and output files
# input_file = 'data/huggingface_train.jsonl'  # Use forward slashes or double backslashes
# output_file = 'data3.jsonl'

# # Transform the structure
# transform_structure(input_file, output_file)


import jsonlines

def transform_structure(input_file, output_file):
    with jsonlines.open(input_file) as reader, jsonlines.open(output_file, mode='w') as writer:
        for obj in reader:
            # Extract necessary fields from the original JSON object
            code = obj.get("code", "")
            api_call = obj.get("api_call", "")
            provider = obj.get("provider", "")
            api_data = obj.get("api_data", {})



            # Extract the domain
            domain = api_data.get('domain', '')

            # Extract the explanation part
            explanation_start = code.find("<<<explanation>>>:") + len("<<<explanation>>>:")
            code_start = code.find("<<<code>>>:")
            if explanation_start != -1 and code_start != -1:
                explanation = code[explanation_start:code_start].strip()
            else:
                explanation = ""

            # Extract the code part
            if "<<<code>>>:" in code:
                code_part = code.split("<<<code>>>:")[1].strip()
            else:
                code_part = ""



            # Construct the new structure
            new_structure = {
                "<<<domain>>>": domain,
                "<<<api_call>>>": api_call,
                "<<<api_provider>>>": provider,
                "<<<explanation>>>": explanation,
                "<<<code>>>": code_part,
                "api_call": api_call,
                "provider": provider,
                "api_data": {
                    "domain": domain,
                    "framework": "Hugging Face Transformers",
                    "functionality": "Feature Extraction",
                    "api_name": api_data.get('api_name', ''),
                    "api_call": api_data.get('api_call', ''),
                    "api_arguments": api_data.get('api_arguments', 'N/A'),
                    "python_environment_requirements": [api_data.get('python_environment_requirements', 'transformers')],
                    "example_code": api_data.get('example_code', 'N/A'),
                    "performance": api_data.get('performance', {"dataset": "N/A", "accuracy": "N/A"}),
                    "description": api_data.get('description', 'A pre-trained ConvBERT model for feature extraction provided by YituTech, based on the Hugging Face Transformers library.')
                }
            }


            # Write the new structure to the output file
            writer.write(new_structure)

# Specify the input and output files
input_file = 'data/huggingface_train.jsonl'  # Use forward slashes or double backslashes
output_file = 'data3.jsonl'

# Transform the structure
transform_structure(input_file, output_file)
