import mediapipe as mp
import cv2
import numpy as np
from os import path
import csv

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        # 실시간으로 카메라에서 들어오는 프레임 변수
        ret, frame = cap.read()

        # 인식 할 색으로
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        result = holistic.process(image)

        image.flags.writeable = True

        # 본래 색으로
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, result.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                  mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1)
                                  )

        try:
            face = result.face_landmarks.landmark
            face_list = []
            # 468개의 얼굴 인식 포인트를 리스트 변수에 저장
            for temp in face:
                face_list.append([temp.x, temp.y, temp.z])

            # 배열을 1차원으로 펼침
            face_row = list(np.array(face_list).flatten())

            # csv 파일이 있는지 확인
            if path.isfile('facedata.csv') == False:
                # ['class', '1', '2' , ... '468']
                landmarks = ['class']
                # 펼친 배열을 csv로 저장
                for val in range(1, len(face) + 1):
                    landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val)]

                with open('facedata.csv', mode='w', newline='') as f:
                    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(landmarks)

            else:
                # 웃는 얼굴 저장
                if cv2.waitKey(1) & 0xFF == ord('1'):
                    face_row.insert(0, 'happy')
                    print('save happy')
                    with open('facedata.csv', mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(face_row)
                # 슬픈 얼굴 저장
                elif cv2.waitKey(1) & 0xFF == ord('2'):
                    face_row.insert(0, 'sad')
                    print('save sad')
                    with open('facedata.csv', mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(face_row)

        except:
            pass

        cv2.imshow('face', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



