from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
torch.manual_seed(30)




def extract_last_lean4_block(text: str) -> str:
    """
    Extract the last ```lean4 ... ``` code block from text.
    Returns only the inner Lean code.
    """
    matches = re.findall(r"```lean4(.*?)```", text, re.DOTALL)
    return matches[-1].strip() if matches else ""


def extract_assistant_response(text: str) -> str:
    segments = re.findall(r"<\|Assistant\|>(.*?)(?=<\|User\||<\|System\||$)", text, re.DOTALL)
    if not segments:
        return text.strip()
    return segments[-1].strip()  


def prove(conversation,max_new_tokens=512):
    model_dir = "/scratch/yj2638/models/deepseek-ai/DeepSeek-Prover-V2-7B"  # or DeepSeek-Prover-V2-671B
    device = "cuda" if torch.cuda.is_available() else "cpu"


    model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.bfloat16, trust_remote_code=True).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    inputs = tokenizer.apply_chat_template(conversation, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,      
            pad_token_id=tokenizer.eos_token_id
        )

    proof = tokenizer.batch_decode(outputs)
    
    # print("---------")
    # print("Complete Proof generated:\n", proof[0])
    # print("---------")

    return extract_last_lean4_block(proof[0])

