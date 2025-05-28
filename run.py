import argparse

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

argparser = argparse.ArgumentParser()
argparser.add_argument("--model-path", type=str, default="9G7B_MHA")
argparser.add_argument("--prompt", type=str, default="山东最高的山是？")
args = argparser.parse_args()

if __name__ == "__main__":
    model_path = args.model_path  # 请替换为你的pytorch_model.bin文件所在的目录的路径
    prompt = args.prompt
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, trust_remote_code=True
    )
    model.to(device)
    model.eval()
    prompt = tokenizer.apply_chat_template(
        conversation=[{"role": "user", "content": prompt}],
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
    ai_answer = responses.strip()
    print(ai_answer)
