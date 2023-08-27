from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os
import openai
import dotenv

## 모델 가져오고 환경 변수, 키값 설정하기
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

key = os.environ["OPENAI_API_KEY"]
openai.api_key = key
##

##  few-shot prompting
def few_shot_prompting(input_target):
    input_text =f'''
    {input_target}와 다른 종류이며, {input_target}와 비슷하지 않는 동물 4마리를 알려주세요, 동물 이름들만 <,>로 구분해서 {input_target}까지 추가하여 영어로 반환해주세요"
    '''
    
    messages=[
            {"role": "system", "content": "사용자의 요청에 대한 답변을 변수 리스트로 보냅니다."},
            {"role": "user", "content": "사자와 다른 종류이며, 사자와 비슷하지 않는 동물 4마리를 알려주세요, 동물 이름들만 <,>로 구분해서 사자까지 추가하여 영어로 반환해주세요"},
            {"role": "assistant", "content": "Leopard, Cheetah, Racer, Fox, Lion"},
            {"role": "user", "content": "하마와 다른 종류이며, 하마와 비슷하지 않는 동물 4마리를 알려주세요, 동물 이름들만 <,>로 구분해서 하마까지 추가하여 영어로 반환해주세요"},
            {"role": "assistant", "content": "Lion, Elephant, Giraffe, Monkey, Hippopotamus"},
            {"role": "user", "content": "강아지와 다른 종류이며, 강아지와 비슷하지 않는 동물 4마리를 알려주세요, 동물 이름들만 <,>로 구분해서 강아지까지 추가하여 영어로 반환해주세요"},
            {"role": "assistant", "content": "Lion, Elephant, Monkey, Cat, Dog"},
            {"role": "user", "content": input_text},
        ]

    chat_completion = openai.ChatCompletion.create( ## gpt 오브젝트 생성후 메세지 전달
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        )

    result = chat_completion.choices[0].message.content  ## gpt결과값 출력
    animals_list=result.split(",")
    return animals_list


def drawing_classification(image_path, animals_list):

    ## Clip 전처리
    animal_list=["a picture of a "+ animal.strip() for animal in animals_list]
    ##
    # image_path="littletales/uploads/개.png"
    # print(f"이미지 경로 :{image_path}")

    ## Clip으로 그림 잘 그려졌는지 판별
    image=Image.open(image_path)
    
    inputs = processor(text=animals_list, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image 
    probs = logits_per_image.softmax(dim=1) 
    

    ## Clip 결과 값 후처리
    value_list = probs.tolist()[0]
    print(f"입력 동물과 비슷한 동물 리스트는 {animals_list}이고 결과는 {value_list}입니다.")
    result= max(value_list)
    reulst_index = value_list.index(result)  # reulst_index - 4 : 올바른 그림 / 나머지는 잘못그림
    print(f"당신의 그림은 {animals_list[reulst_index]}와 더 비슷합니다")
    return reulst_index


def chat_drawing_check(user_input_text,image_path):
    animals_list= few_shot_prompting(user_input_text)
    check_picture=drawing_classification(image_path,animals_list)

    if check_picture==4:
        return True
    else:
        return False