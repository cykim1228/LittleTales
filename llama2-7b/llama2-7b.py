# import os
# from huggingface_hub import login

# login(token=os.environ.get("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")) #예찬 계정

from transformers import AutoTokenizer
import transformers
import torch

model2 = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(
    model2,
    use_auth_token=True,
)

pipeline2 = transformers.pipeline(
    "text-generation",
    model=model2,
    torch_dtype=torch.float16,
    device_map="auto",
)

def gen2(x, max_length):
    sequences = pipeline2(
        x,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=max_length,
    )

    return sequences[0]["generated_text"].replace(x, "")


print(gen2("Please make a fairy tale with the main character 'Lion' for the children's audience. Be creative and don't worry, and make a great fictional story for children",1500))