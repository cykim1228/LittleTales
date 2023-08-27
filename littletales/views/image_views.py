#이미지 불러오기
#
# 누끼 따기
#
# 이미지 저장
#
# dall-e 2써서 프롬프트
#
# 이미지 생성


from PIL import Image
import requests
import os
import openai
import dotenv
import json
from PIL import Image

# from flask import Blueprint
# from matplotlib import pyplot as plt
# from rembg import remove
# openai.organization = "org-9wDldVZ1upcx03krVviK4tWw"
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.Model.list()

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

openai.organization = "org-jUejdT5GvU7fyKtp3IAwwin9"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

##key file 값 불러오기
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
key = os.environ["OPENAI_API_KEY"]
openai.api_key = key
##
#PIL저장
from PIL import Image


# 라이브러리 임포트
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

#bp = Blueprint('littleimage', __name__, url_prefix='/littleimage')

# 이미지 불러오기
image_path = "D:/projects/littletales/littletales/uploads/dog.png"
image = Image.open(image_path)
print("이미지 불러오기")

# 배경 제거
output = remove(image)
print("배경 제거")

# 이미지 저장 (rembg.png 로 저장)
output.save('rembg.png')
print("이미지 저장")

# 프롬프트 입력
prompt = input("depict the background as a fairy tale with the characteristics of the painting: ")
#
# # 프롬프트를 토큰화
#inputs = tokenizer(prompt, return_tensors="pt")
#print("프롬프트")

# 이미지 생성
response = openai.Image.create_edit(
  image=open("rembg.png", "rb"),  # 수정된 파일 이름
  mask=open("rembg.png", "rb"),   # 수정된 파일 이름
  prompt=prompt,
  n=1,
  size="1024x1024"
)
print("이미지 생성")

# 생성된 이미지 플롯
# image = response.edits[0].image
# image.save('result.png')
# print("생성된 이미지 플롯")

# image_url = response['data'][0]['url']
#
# with torch.no_grad():
#     outputs = model.generate_images(**inputs)
#
# import matplotlib.pyplot as plt


image_url = response['data'][0]['url']

##생성된 이미지 url값을 가져온다
im = Image.open(requests.get(image_url, stream=True).raw)
im.show()




# from PIL import Image
# import requests
# import os
# import openai
# import dotenv
# import json
# from PIL import Image
#
# ##key file 값 불러오기
# dotenv_file = dotenv.find_dotenv()
# dotenv.load_dotenv(dotenv_file)
# key = os.environ["OPENAI_API_KEY"]
# openai.api_key = key
# ##
#
# ##image generation
# response = openai.Image.create(
#   prompt="a white siamese cat",
#   n=1,
#   size="1024x1024"
# )
# image_url = response['data'][0]['url']
#
# ##생성된 이미지 url값을 가져온다
# im = Image.open(requests.get(image_url, stream=True).raw)
# im.show()
#
# #PIL저장
# from PIL import Image
#
# # 이미지를 불러오고 처리하는 등의 코드가 있겠죠?
# img = Image.open('imagepath+file')
#
# # 저장해봅시다.
# img.save('sample.png', 'png')
#
# # 특정 폴더에 저장하려면
# # 저장하고자 하는 폴더의 절대경로를 입력해주면 됩니다.
# # 경로 앞에 / 가 들어가줘야된다는걸 기억!!
# img.save('/content/data/output.png', 'png')
#
# #경우에 따라 상대경로를 입력해도 됩니다.
# img.save('./data/output.png', 'png')
#
#
#
# # 이미지를 엽니다.
# img = Image.open('example.jpg')
#
# # 다른 형식으로 이미지를 저장합니다.
# img.save('example.png', 'PNG')