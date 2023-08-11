from flask import Blueprint, render_template
from flask import url_for
from flask import Blueprint, request, render_template
from werkzeug.utils import redirect
import os
import openai
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('littlechat', __name__, url_prefix='/littlechat')

@bp.route('/')
def chat_index() :
    return render_template('little_chat.html')

@bp.route('/chat', methods=['GET', 'POST'])
def chat():
    openai.api_key = "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"

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

