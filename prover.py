from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
torch.manual_seed(30)


def prove(conversation):
    model_dir = "/scratch/yj2638/models/deepseek-ai/DeepSeek-Prover-V2-7B"  # or DeepSeek-Prover-V2-671B
    device = "cuda" if torch.cuda.is_available() else "cpu"


    model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.bfloat16, trust_remote_code=True).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    inputs = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)

    import time
    start = time.time()
    outputs = model.generate(inputs, max_new_tokens=1024)
    proof = tokenizer.batch_decode(outputs)
    return proof[0]

