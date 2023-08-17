import dotenv
from flask import Blueprint, render_template
from flask import url_for
from flask import Blueprint, request, render_template
from werkzeug.utils import redirect
import os
import openai

bp = Blueprint('littleread', __name__, url_prefix='/littleread')

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

key = os.environ["OPENAI_API_KEY"]

@bp.route('/', methods=['POST'])
def read_index() :
    animal_name = request.form.get('animal')
    print('판별된 동물 : ', animal_name)

    chat_response = None

    if animal_name:
        chat_response = make(animal_name)

    print('생성 동화 : ', chat_response)
    return render_template('little_read.html', animal_name=animal_name, chat_response=chat_response)

def make(animal_name):
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
        max_tokens=500,  # 원하는 답변의 최대 토큰 길이를 설정하세요 (300자 이상의 답변을 원하시면 조정)
        stop=["\n"]
    )

    print('리스폰스 : ', response)
    result = response.choices[0].message.content.strip()

    print('답변 : ', result)

    return result
