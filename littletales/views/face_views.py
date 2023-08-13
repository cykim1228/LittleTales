from flask import Blueprint, render_template, Response, request
from flask import url_for
from werkzeug.utils import redirect

import cv2
import mediapipe as mp
import numpy as np
import joblib
import pandas as pd

# 쓸데없는 경고문 지우기
import warnings

bp = Blueprint('littleface', __name__, url_prefix='/littleface')

warnings.filterwarnings('ignore')

# 모델 가져오기
model = joblib.load('littletales/machine/face.pkl')

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

yhat_result = ''

camera = cv2.VideoCapture(0)


def gen_frames():  # generate frame by frame from camera
    global yhat_result  # yhat_result 값을 수정하기 위해 global 키워드 사용

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

        while True:
            # Capture frame-by-frame
            success, frame = camera.read()  # read the camera frame

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            result = holistic.process(image)

            image.flags.writeable = True

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(image, result.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                      mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
                                      )

            try:
                face = result.face_landmarks.landmark

                face_list = []
                for temp in face:
                    face_list.append([temp.x, temp.y, temp.z])
                face_row = list(np.array(face_list).flatten())

                X = pd.DataFrame([face_row])
                cname = ['sad', 'happy']
                # 결과값
                yhat = model.predict(X)[0]
                # 정답데이터
                yhat_result = cname[yhat]

                # print('표정 : ', yhat_result)
                # print(yhat_result)

                if yhat_result == 'happy':
                    print('카메라 종료 / yhat_result : ', yhat_result)
                    break

            except:
                pass

            else:
                # print('if문 안탐 / yhat_result : ', yhat_result)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@bp.route('/')
def face_index() :

    return render_template('little_face.html', yhat_result=yhat_result)


@bp.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/classification', methods=['POST'])
def classification():
    animal_name = request.form.get('animal')  # 동물 이미지 파일명 받기
    if animal_name:
        print("Happy 동물: ", animal_name)  # 'happy'일 때 해당 동물 이미지 파일명 출력 또는 저장

    return redirect(url_for('littlechat.chat_index', animal=animal_name))

@bp.route('/check_happy_status')
def check_happy_status():
    if yhat_result == 'happy':
        print('(happy)yhat_result : ', yhat_result)
        return 'happy'

    else:
        print('(sad)yhat_result : ', yhat_result)
        return 'not_happy'
