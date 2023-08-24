import base64
import os

from flask import Blueprint, request, render_template, jsonify

bp = Blueprint('littledraw', __name__, url_prefix='/littledraw')

UPLOAD_FOLDER = 'uploads'

@bp.route('/')
def draw_index() :

    return render_template('little_input.html')

@bp.route('/canvas', methods=['POST'])
def draw_canvas() :
    animal_name = request.form.get('animal')
    print('판별된 동물 : ', animal_name)

    return render_template('little_draw.html', animal_name=animal_name)


@bp.route('/upload_image', methods=['POST'])
def upload_image():
    data = request.json
    image_data = data.get('image')
    animal_name = data.get('animal_name')

    if image_data and animal_name:
        # 이미지 데이터를 base64로 디코딩하여 이미지 파일로 저장
        image_data = image_data.replace("data:image/png;base64,", "")
        image_path = os.path.join('littletales', UPLOAD_FOLDER, f"{animal_name}.png")

        with open(image_path, "wb") as image_file:
            image_file.write(base64.b64decode(image_data))

        return jsonify({"message": "Image uploaded successfully."}), 200

    return jsonify({"message": "Invalid image data or animal name."}), 400
