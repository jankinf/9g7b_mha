import argparse
import json
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

argparser = argparse.ArgumentParser()
argparser.add_argument("--config_file", type=str, default="SourceCode/config.json")
args = argparser.parse_args()

with open(args.config_file, "r") as f:
    config = json.load(f)
    system = config["system"]

    input_dir = system.get("inputPath", "./Dataset")
    output_dir = system.get("outputPath", "./Output")
    model_dir = system.get("modelPath", "./Model")

    task_json = os.path.join(input_dir, "meta.json")
    model_dir = os.path.join(model_dir, "9G7B_MHA")

if __name__ == "__main__":
    result_json_file = f"{output_dir}/result.json"
    os.makedirs(output_dir, exist_ok=True)

    with open(task_json, "r", encoding="utf-8") as fp:
        data = json.load(fp)

    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, torch_dtype=torch.bfloat16, trust_remote_code=True
    )
    model.to(device)
    model.eval()

    results = []
    for data_dict in data:
        raw_prompt = data_dict["prompt"]
        prompt_id = data_dict["id"]

        prompt = tokenizer.apply_chat_template(
            conversation=[{"role": "user", "content": raw_prompt}],
            add_generation_prompt=True,
            tokenize=False,
        )
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs.to(model.device)
        with torch.no_grad():
            res = model.generate(**inputs, max_new_tokens=256)
        responses = tokenizer.decode(
            res[0][inputs.input_ids.shape[1] :], skip_special_tokens=True
        )
        answer = responses.strip()

        results.append({"id": prompt_id, "prompt": raw_prompt, "response": answer})

    with open(result_json_file, "w", encoding="utf-8") as fp:
        json.dump(results, fp, indent=4, ensure_ascii=False)
