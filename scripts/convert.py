import json

with open('instructions-dataset.jsonl',encoding="utf-8") as f:
    instructions = [json.loads(line) for line in f]
for i in instructions :
    instruction = {"text": i}
    print(instruction)
    
    with open('data/final_ins.jsonl', 'a', encoding="utf-8") as fw:
        fw.write(json.dumps(instruction, ensure_ascii=False) + '\n')
        fw.close()



        #  with open('data/seed.jsonl', 'a', encoding="utf-8") as fw:
        #         fw.write(json.dumps(instruction, ensure_ascii=False) + '\n')
        #         fw.close()
        # else:
        #     None