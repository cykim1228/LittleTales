import base64

from PIL import Image
import requests
import os
import openai
import dotenv
from flask import Blueprint, request, render_template
from rembg import remove
#필요 없음
#from transformers import GPT2Tokenizer
import json
from littletales.gpt_function.check_drawing import chat_drawing_check

#플라스크 부분은 주석처리 해 둠
#from flask import Blueprint
#from matplotlib import pyplot as plt
# openai.organization = "org-9wDldVZ1upcx03krVviK4tWw"
bp = Blueprint('littleimage', __name__, url_prefix='/littleimage')

# key file 값 불러오기 (환경변수 로딩)
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# API 키 설정
openai.organization = "org-jUejdT5GvU7fyKtp3IAwwin9"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

animal_name=''
image_path=''

# 위 코드랑 중복되는 거라 일단 둘 중 뭐가 맞는 지 헷갈려서 주석처리
# key = os.environ["OPENAI_API_KEY"]
# openai.api_key = key

@bp.route('/', methods=['POST'])
def image_index() :
    animal_name = request.form.get('animal_name')
    print('판별된 동물 : ', animal_name)

    # 전송된 이미지 데이터 받아오기
    image_data = request.files.get('image')

    # 이미지 데이터를 파일로 저장 (uploads 폴더에 저장)
    uploaded_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'uploaded_image.png')
    image_data.save(uploaded_image_path)

    # 이미지 불러오기
    # image_path = os.path.join('uploads', 'dog.png')
    image = Image.open(uploaded_image_path)
    print("이미지 불러오기 완료")

    # 배경 제거
    output = remove(image)
    print("배경 제거 완료")

    # 이미지 저장 (rembg.png 로 저장)
    rembg_path = os.path.join('generated', 'rembg.png')
    output.save('rembg.png')
    print("배경제거된 이미지 저장 완료")

    prompt = "depict the background as a fairy tale with the characteristics of the painting "
    print("프롬프트 입력 완료")

    # 이미지 생성
    response = openai.Image.create_edit(
        image=open("rembg.png", "rb"),  # 수정된 파일 이름
        mask=open("rembg.png", "rb"),  # 수정된 파일 이름
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    print("이미지 생성 완료")
    image_url = response['data'][0]['url']

    # 생성된 이미지 다운로드 및 저장
    generated_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated', 'generated_image.png')
    image_response = requests.get(image_url)
    with open(generated_image_path, "wb") as f:
        f.write(image_response.content)
    print("이미지 저장 완료")

    return render_template('little_read.html', animal_name=animal_name, image_response=image_response)

@bp.route('/image_check', methods=['POST'])
def image_check() :
    image_path='littletales/generated/generated_image.png'
    if chat_drawing_check(animal_name,image_path):
        response="잘 그림"
    else:
        response="못 그림"

    return response

# # GPT-2 토크나이저 로드
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# 프롬프트 입력
# 그림의 특징과 함께 배경을 동화로 묘사합니다.

# # 프롬프트를 토큰화_방법1
# #inputs = tokenizer(prompt, return_tensors="pt")
# # 프롬프트를 토큰화_방법2
# tokens = tokenizer.tokenize(prompt)
# token_ids = tokenizer.convert_tokens_to_ids(tokens)

# 굳이 안필요할거같아서 주석처리
# print("토큰화된 프롬프트:", tokens)
# print("토큰 ID:", token_ids)

# 이미지를 열어서 보여주기
# image = Image.open("generated_image.png")
# image.show()
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
