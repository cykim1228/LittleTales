import dotenv
from flask import Blueprint, render_template
from flask import url_for
from flask import Blueprint, request, render_template
from werkzeug.utils import redirect
import os
import openai

bp = Blueprint('littlechat', __name__, url_prefix='/littlechat')

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

key = os.environ["OPENAI_API_KEY"]

@bp.route('/')
def chat_index() :
    animal_name = request.args.get('animal')
    print('판별된 동물 : ', animal_name)

    return render_template('little_chat.html', animal_name=animal_name)

@bp.route('/chat', methods=['GET', 'POST'])
def chat():
    openai.api_key = key

    chat_text = request.form['question']
    print('질문 : ', chat_text)

    messages = [
        {
            "role" : "user",
            "content" : chat_text
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

    print('리스폰스 : ', response)
    result = [response.choices[0].message.content.strip()]

    print('답변 : ', result)

    return result


def make(animal_name):
    openai.api_key = key

    chat_text = f"Tell me a fairy tale starring {animal_name} in Korean"
    print('질문 : ', chat_text)

    messages = [
        {
            "role": "user",
            "content": chat_text
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

    print('리스폰스 : ', response)
    result = response.choices[0].message.content.strip()

    print('답변 : ', result)

    return result
