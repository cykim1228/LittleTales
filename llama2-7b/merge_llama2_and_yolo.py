
from ultralytics import YOLO
from transformers import AutoTokenizer
import transformers
import torch
import deepl
import os
from huggingface_hub import HfApi, Repository

#deepl인증키 및 메소드 가져오기
deepl_key = "d7ff04a7-09eb-0c77-558a-27575e0361d4:fx"
translator = deepl.Translator(deepl_key)

#허깅페이스 인증키 가져오기
hugging_face_key ="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"
hf_token = os.environ.get(hugging_face_key)  
api = HfApi()
api.token = hf_token

#동물 클래스 생성
animals=['Bear', 'Cat', 'Dog', 'Duck', 'Lion', 'Panda', 'Rabbit', 'Tiger', 'Turtle']

#모델 추론
print("모델추론 시작")
mode_yolo = YOLO('../yolo/yolo_model.pt')
results = mode_yolo.predict(source='../yolo/lion.jpg',show=False,save=False)
print("모델추론 끝")

#후처리(욜로에서 디텍딩된 동물 이름 판별)
result_animals_name=[]
results_group=results[0].boxes.cls #입력 사진에서 해당되는 클래스가 실수형 변수로 나옴
for index in results_group.tolist(): 
    animal_name=animals[int(index)] #실수형 변수를 동물이름으로 변경
    if animal_name not in result_animals_name: # 중복되는 동물이름 없앰
        result_animals_name.append(animal_name)

#(결과)
# print(result_animals_name)


print("라마2 다운")

##라마 다운 및 전처리
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

answer = gen2(f"Please make a fairy tale with the main character {result_animals_name} for the children's audience. Be creative and don't worry, and make a great fictional story for children",1500)
result = translator.translate_text(answer, target_lang="ko")
print(result)