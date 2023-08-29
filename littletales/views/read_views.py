import base64
import io

import dotenv
import torch
import transformers
from deepl import translator
from flask import Blueprint, render_template
from flask import url_for
from flask import Blueprint, request, render_template
from werkzeug.utils import redirect
import os
import openai
from transformers import AutoTokenizer
from huggingface_hub import HfApi, Repository
import deepl
from PIL import Image
import requests
import os
import openai
import dotenv
from flask import Blueprint, request, render_template, jsonify, session
from rembg import remove
from base64 import decodebytes
from littletales.gpt_function.make_title_GPT import make_story

bp = Blueprint('littleread', __name__, url_prefix='/littleread')

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

key = os.environ["OPENAI_API_KEY"]

# API 키 설정
openai.organization = "org-jUejdT5GvU7fyKtp3IAwwin9"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

# # deepl인증키 및 메소드 가져오기
# deepl_key = "d7ff04a7-09eb-0c77-558a-27575e0361d4:fx"
# translator = deepl.Translator(deepl_key)
#
# # 허깅페이스 인증키 가져오기
# # 터미널에서 허깅페이스 로그인 선작업 해야함
# # huggingface-cli login
# hugging_face_key ="hf_wxwkJyjXaHNbvtwEfwFZqDdQEiTFJSuiFAD"
# hf_token = os.environ.get(hugging_face_key)
# api = HfApi()
# api.token = hf_token
#
# model_llama2 = "meta-llama/Llama-2-7b-chat-hf"
#
# tokenizer = AutoTokenizer.from_pretrained(
#     model_llama2,
#     use_auth_token=True,
# )
#
# pipeline = transformers.pipeline(
#     "text-generation",
#     model=model_llama2,
#     torch_dtype=torch.float16,
#     device_map="auto",
# )

@bp.route('/', methods=['POST'])
def read_index() :

    print('리퀘스트 : ', request)
    print('리퀘스트 키워드 : ', request.form['animal'])
    print('리퀘스트 이미지 : ', request.form.get('image'))

    animal_name = request.form['animal']
    image_data_url = request.form['image']
    target = animal_name
    title = request.form['title']
    plot = request.form['plot']

    result_list = make_story(target, title, plot)

    print('결과 값 : ', result_list)

    backgrounds = [result_list[2][0], result_list[2][1], result_list[2][2],result_list[2][3]]
    images = []

    header, image_data_base64 = image_data_url.split(',', 1)
    image_data = base64.b64decode(image_data_base64)

    print('판별된 동물 : ', animal_name)

    # 이미지 데이터를 임시 파일로 저장
    generated_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated', 'temp_image.png')

    with open(generated_image_path, "wb") as f:
        f.write(image_data)

    print('이미지 저장 완료 :', generated_image_path)

    # 이미지 데이터를 직접 로드합니다.
    with open(generated_image_path, "rb") as f:
        actual_image_data = f.read()

    for background in backgrounds:
        image_name = gen_image(actual_image_data, background)
        images.append(image_name)

    image_response = images

    chat_response = None

    # if animal_name:
        # chat_response = make_llama(animal_name)
        # chat_response = make_gpt(animal_name)

    print('키워드 : ', animal_name)
    print('생성 동화 : ', chat_response)
    print('이미지 경로 : ', image_response)

    session['animal_name'] = animal_name

    session['title_response1'] = result_list[0][0]
    session['title_response2'] = result_list[0][1]
    session['title_response3'] = result_list[0][2]
    session['title_response4'] = result_list[0][3]

    session['chat_response1'] = result_list[1][0]
    session['chat_response2'] = result_list[1][1]
    session['chat_response3'] = result_list[1][2]
    session['chat_response4'] = result_list[1][3]

    session['place_response1'] = result_list[2][0]
    session['place_response2'] = result_list[2][1]
    session['place_response3'] = result_list[2][2]
    session['place_response4'] = result_list[2][3]

    session['image_response1'] = image_response[0]
    session['image_response2'] = image_response[1]
    session['image_response3'] = image_response[2]
    session['image_response4'] = image_response[3]

    title_response1 = result_list[0][0]
    chat_response1 = result_list[1][0]
    place_response1 = result_list[2][0]
    image_response1 = image_response[0]

    return render_template('little_read_1.html', animal_name=animal_name, title_response1=title_response1, chat_response1=chat_response1, place_response1=place_response1, image_response1=image_response1)


@bp.route('/read_one')
def read_one() :

    image_response1 = session.get('image_response1')
    chat_response1 = session.get('chat_response1')
    title_response1 = session.get('title_response1')
    place_response1 = session.get('place_response1')

    return render_template('little_read_1.html', title_response1=title_response1, chat_response1=chat_response1, place_response1=place_response1, image_response1=image_response1)

@bp.route('/read_two')
def read_two() :

    image_response2 = session.get('image_response2')
    chat_response2 = session.get('chat_response2')
    title_response2 = session.get('title_response2')
    place_response2 = session.get('place_response2')

    return render_template('little_read_2.html', title_response2=title_response2, chat_response2=chat_response2, place_response2=place_response2, image_response2=image_response2)

@bp.route('/read_three')
def read_three() :

    image_response3 = session.get('image_response3')
    chat_response3 = session.get('chat_response3')
    title_response3 = session.get('title_response3')
    place_response3 = session.get('place_response3')

    return render_template('little_read_3.html', title_response3=title_response3, chat_response3=chat_response3, place_response3=place_response3, image_response3=image_response3)

@bp.route('/read_four')
def read_four() :

    image_response4 = session.get('image_response4')
    chat_response4 = session.get('chat_response4')
    title_response4 = session.get('title_response4')
    place_response4 = session.get('place_response4')

    return render_template('little_read_4.html', title_response4=title_response4, chat_response4=chat_response4, place_response4=place_response4, image_response4=image_response4)

def gen_image(image_data, background) :
    # 이미지 데이터를 PIL.Image 형식으로 열기
    image = Image.open(io.BytesIO(image_data))
    print("이미지 불러오기 완료")

    # 배경 제거
    output = remove(image)
    print("배경 제거 완료")

    # 이미지 저장 (rembg.png 로 저장)
    rembg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated', 'rembg.png')
    output.save(rembg_path)
    print("배경제거된 이미지 저장 완료 : ", rembg_path)

    # 주어진 배경 키워드를 사용하여 프롬프트를 설정
    #prompt = f"depict the background as a {background} fairy tale with the characteristics of the painting"
    prompt = f"make {background} based on painting features like fairy tale, make be colorful except literal"
    print("프롬프트 입력 완료 : ", prompt)

    # 이미지 생성
    response = openai.Image.create_edit(
        image=open(rembg_path, "rb"),  # 수정된 파일 이름
        mask=open(rembg_path, "rb"),  # 수정된 파일 이름
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response['data'][0]['url']
    print("이미지 생성 완료 : ", image_url)

    # 생성된 이미지 다운로드 및 저장
    from datetime import datetime
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    generated_image_name = f'generated_image_{background}_{current_time}.png'
    generated_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated', generated_image_name)
    image_response = requests.get(image_url)
    with open(generated_image_path, "wb") as f:
        f.write(image_response.content)
    print("이미지 저장 완료 : ", generated_image_path)

    return generated_image_name



def make_gpt(animal_name):
    openai.api_key = key

    chat_text = f"'{animal_name}'가 주인공이고 교훈을 주는 동화를 10 장 분량으로 기승전결에 맞춰서 만들어줘"
    # chat_text = f"Tell me a fairy tale starring {animal_name} in Korean"
    print('질문 : ', chat_text)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates fairy tales."
        },
        {
            "role": "user",
            "content": chat_text
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,  # 다양한 답변을 유도하기 위해 온도를 조정해보세요 (기본값은 1.0)
        max_tokens=1000,  # 원하는 답변의 최대 토큰 길이를 설정하세요 (300자 이상의 답변을 원하시면 조정)
        stop=["\n"]
    )

    print('리스폰스 : ', response)
    result = response.choices[0].message.content.strip()

    print('답변 : ', result)

    return result

# def make_llama(animal_name) :
#     print('동물 : ', animal_name)
#
#     while True :
#         answer = gen2(
#             f"Please make a fairy tale with the main character {animal_name} for the children's audience. Be creative and don't worry, and make a great fictional story for children",
#             1500)
#         print('answer : ', answer)
#         if len(str(answer)) > 200 :
#             break
#
#     result = translator.translate_text(answer, target_lang="ko")
#     result = str(result).strip().split("\n")
#
#     result_str = ""
#     for i in result:
#         if (len(i) > 4):
#             # print(i)
#             result_str += i + "\n"
#
#     result_str += '-끝-'
#
#     print('답변 : ', result_str)
#
#     return result_str
#
# def gen2(x, max_length):
#     sequences = pipeline(
#         x,
#         do_sample=True,
#         top_k=10,
#         num_return_sequences=1,
#         eos_token_id=tokenizer.eos_token_id,
#         max_length=max_length,
#     )
#
#     return sequences[0]["generated_text"].replace(x, "")