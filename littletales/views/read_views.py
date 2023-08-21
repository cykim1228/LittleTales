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

bp = Blueprint('littleread', __name__, url_prefix='/littleread')

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

key = os.environ["OPENAI_API_KEY"]

# deepl인증키 및 메소드 가져오기
deepl_key = "d7ff04a7-09eb-0c77-558a-27575e0361d4:fx"
translator = deepl.Translator(deepl_key)

# 허깅페이스 인증키 가져오기
# 터미널에서 허깅페이스 로그인 선작업 해야함
# huggingface-cli login
hugging_face_key ="hf_wxwkJyjXaHNbvtwEfwFZqDdQEiTFJSuiFAD"
hf_token = os.environ.get(hugging_face_key)
api = HfApi()
api.token = hf_token

model_llama2 = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(
    model_llama2,
    use_auth_token=True,
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model_llama2,
    torch_dtype=torch.float16,
    device_map="auto",
)

@bp.route('/', methods=['POST'])
def read_index() :
    animal_name = request.form.get('animal')
    print('판별된 동물 : ', animal_name)

    chat_response = None

    if animal_name:
        chat_response = make_llama(animal_name)

    print('생성 동화 : ', chat_response)
    return render_template('little_read.html', animal_name=animal_name, chat_response=chat_response)

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

def make_llama(animal_name) :
    print('동물 : ', animal_name)

    while True :
        answer = gen2(
            f"Please make a fairy tale with the main character {animal_name} for the children's audience. Be creative and don't worry, and make a great fictional story for children",
            1500)
        print('answer : ', answer)
        if len(str(answer)) > 200 :
            break

    result = translator.translate_text(answer, target_lang="ko")
    result = str(result).strip().split("\n")

    result_str = ""
    for i in result:
        if (len(i) > 4):
            # print(i)
            result_str += i + "\n"

    result_str += '-끝-'

    print('답변 : ', result_str)

    return result_str

def gen2(x, max_length):
    sequences = pipeline(
        x,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=max_length,
    )

    return sequences[0]["generated_text"].replace(x, "")