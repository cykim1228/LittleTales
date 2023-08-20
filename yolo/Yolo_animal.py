from ultralytics import YOLO

#동물 클래스 생성
animals=['Bear', 'Cat', 'Dog', 'Duck', 'Lion', 'Panda', 'Rabbit', 'Tiger', 'Turtle']

#모델 추론
model = YOLO('F:\PycharmProjects\littleTales\yolo\yolo_model.pt')
results = model.predict(source='F:\PycharmProjects\littleTales\yolo\lion.jpg',show=False,save=False)


#후처리(욜로에서 디텍딩된 동물 이름 판별)
result_animals_name=[]
results_group=results[0].boxes.cls #입력 사진에서 해당되는 클래스가 실수형 변수로 나옴
for index in results_group.tolist(): 
    animal_name=animals[int(index)] #실수형 변수를 동물이름으로 변경
    if animal_name not in result_animals_name: # 중복되는 동물이름 없앰
        result_animals_name.append(animal_name)

#(결과)
print(result_animals_name)
