from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask import url_for
from werkzeug.utils import redirect
from ultralytics import YOLO
import os

bp = Blueprint('littleyolo', __name__, url_prefix='/littleyolo')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def yolo_index() :

    return render_template('little_yolo.html')

@bp.route('/upload_and_detect', methods=['POST'])
def upload_and_detect():
    result_animals_name = []

    if 'photo' in request.files:
        file = request.files['photo']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('littletales', 'uploads', filename)
            file.save(file_path)

            # 모델 추론
            model_path = os.path.join('littletales', 'machine', 'yolo_model.pt')  # YOLO 모델 경로 수정
            model = YOLO(model_path)
            results = model.predict(source=file_path, show=False, save=False)

            # 동물 클래스 생성
            animals = ['Bear', 'Cat', 'Dog', 'Duck', 'Lion', 'Panda', 'Rabbit', 'Tiger', 'Turtle']
            results_group = results[0].boxes.cls

            # 후처리(욜로에서 디텍딩된 동물 이름 판별)
            for index in results_group.tolist():
                animal_name = animals[int(index)]
                if animal_name not in result_animals_name:
                    result_animals_name.append(animal_name)

            return jsonify({"result": ', '.join(result_animals_name)})
        else:
            return jsonify({"result": "올바른 파일 형식을 업로드하세요."})
    else:
        return jsonify({"result": "파일이 전송되지 않았습니다."})
