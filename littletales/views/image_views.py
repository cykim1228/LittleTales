from diffusers import DiffusionPipeline
import torch
from flask import Blueprint

bp = Blueprint('littleimage', __name__, url_prefix='/littleimage')

pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
pipe.to("cuda")

prompt1 = "a smiling puppy"
prompt2 = "a smiling kitten"

images = pipe(prompt=prompt1).images[0]
images2 = pipe(prompt=prompt2).images[0]
