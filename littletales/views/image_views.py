from PIL import Image
import requests
import os
import openai
import dotenv
from rembg import remove
from transformers import GPT2Tokenizer
import json

#플라스크 부분은 주석처리 해 둠
#from flask import Blueprint
#from matplotlib import pyplot as plt
# openai.organization = "org-9wDldVZ1upcx03krVviK4tWw"
#bp = Blueprint('littleimage', __name__, url_prefix='/littleimage')

# key file 값 불러오기 (환경변수 로딩)
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# API 키 설정
openai.organization = "org-jUejdT5GvU7fyKtp3IAwwin9"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

# 위 코드랑 중복되는 거라 일단 둘 중 뭐가 맞는 지 헷갈려서 주석처리
# key = os.environ["OPENAI_API_KEY"]
# openai.api_key = key

# 이미지 불러오기
image_path = "D:/projects/littletales/littletales/uploads/dog.png"
image = Image.open(image_path)
print("이미지 불러오기 완료")

# 배경 제거
output = remove(image)
print("배경 제거 완료")

# 이미지 저장 (rembg.png 로 저장)
output.save('rembg.png')
print("배경제거된 이미지 저장 완료")

# GPT-2 토크나이저 로드
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# 프롬프트 입력
prompt = input("depict the background as a fairy tale with the characteristics of the painting: ")

# 프롬프트를 토큰화_방법1
#inputs = tokenizer(prompt, return_tensors="pt")
# 프롬프트를 토큰화_방법2
tokens = tokenizer.tokenize(prompt)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

print("프롬프트 입력 완료")

# 굳이 안필요할거같아서 주석처리
# print("토큰화된 프롬프트:", tokens)
# print("토큰 ID:", token_ids)

# 이미지 생성
response = openai.Image.create_edit(
  image=open("rembg.png", "rb"),  # 수정된 파일 이름
  mask=open("rembg.png", "rb"),   # 수정된 파일 이름
  prompt=prompt,
  n=1,
  size="1024x1024"
)
print("이미지 생성")

image_url = response['data'][0]['url']

# 생성된 이미지 플롯
# image = response.edits[0].image
# image.save('result.png')
# print("생성된 이미지 플롯")

# image_url = response['data'][0]['url']
#
# with torch.no_grad():
#     outputs = model.generate_images(**inputs)

# 생성된 이미지 url값을 가져온다
# im = Image.open(requests.get(image_url, stream=True).raw)
# im.show()
# ##key file 값 불러오기
# dotenv_file = dotenv.find_dotenv()
# dotenv.load_dotenv(dotenv_file)
# key = os.environ["OPENAI_API_KEY"]
# openai.api_key = key
