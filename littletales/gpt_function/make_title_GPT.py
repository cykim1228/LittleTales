from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
import os
import openai
import dotenv
import json

## 모델 가져오고 환경 변수, 키값 설정하기
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

key = os.environ["OPENAI_API_KEY"]
openai.api_key = key
##

##  few-shot prompting


def make_title(animal_name):

    system_text='''
    1 - 사용자가 입력하는 동물로 5~8세의 어린이들이 좋아할만한 동화를 만들꺼야
    2 - 동화의 제목과 내용을 2줄 정도 간략하게 3가지 말해줘
    3- 동화의 제목을 <title>에 저장하고 동화의 내용들을 <content>에 저장해 주인공 이름을 정해주지마
    4- Json형식으로 출력해줘
    '''

    user_list=["돼지","코끼리","개"]

    assistant1='''
    {
    "fairytale": [
    {
        "title": "돼지마을 모험",
        "content": "한 작은 돼지 가족이 모험을 떠납니다. 함께 여러 동물 친구들을 만나며 즐거운 경험을 합니다."
    },
    {
        "title": "우주 여행 뚜루뚜루 돼지",
        "content": "돼지마을의 뚜루뚜루 돼지가 우주선을 타고 화려하고 신비로운 우주 여행을 떠나게 됩니다. 마을 주민들은 뚜루뚜루 돼지의 모험을 응원합니다."
    },
    {
        "title": "도전! 돼지와 늑대의 우정",
        "content": "한 돼지와 늑대가 우정을 키우기 위해 도전을 합니다. 함께 어려운 과제를 해결하며 서로를 이해하고 지지합니다."
    }
    ]
    }
    '''
    assistant2='''
    {
    "fairytale": [
    {
        "title": "코끼리의 꿈",
        "content": "작은 코끼리가 자신의 꿈을 이루기 위해 모험을 떠납니다. 여러 동물 친구들과 함께 힘을 합쳐 어려움을 극복하고 꿈을 실현합니다."
    },
    {
        "title": "코끼리 왕국의 비밀",
        "content": "코끼리 왕국에서 비밀이 발견되었습니다. 작은 코끼리가 비밀을 해결하기 위해 모험을 떠나며 코끼리들의 도움을 받습니다. 결국 왕국을 구하는 비밀을 알게됩니다."
    },
    {
        "title": "용감한 코끼리의 대모험",
        "content": "용감한 코끼리가 자신의 용기를 시험하기 위해 위험한 대모험에 도전합니다. 여러 동물 친구들과 함께하며 용감함과 용감한 결심을 배우게 됩니다."
    }
    ]
    }
    '''
    assistant3='''
    {
    "fairytale": [
    {
        "title": "개와 주인의 우정",
        "content": "한 개와 주인이 서로를 이해하고 함께하는 이야기입니다. 어려움을 겪으면서도 서로를 지지하고 힘을 내며 우정을 다지게 됩니다."
    },
    {
        "title": "말썽꾸러기 개의 모험",
        "content": "말썽꾸러기 개가 모험을 떠나게 됩니다. 여러 동물 친구들과 함께 재미있는 일들을 겪으며 새로운 경험을 쌓습니다."
    },
    {
        "title": "용감한 개의 대모험",
        "content": "용감한 개가 위험한 대모험에 도전하게 됩니다. 다양한 동물 친구들과 함께 어려움을 극복하고 용감한 행동을 보이며 모험을 성공시킵니다."
    }
    ]
    }
    '''

    messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_list[0]},
            {"role": "assistant", "content": assistant1},
            {"role": "user", "content": user_list[1]},
            {"role": "assistant", "content": assistant2},
            {"role": "user", "content": user_list[2]},
            {"role": "assistant", "content": assistant3},
            {"role": "user", "content": animal_name},
        ]

    chat_completion = openai.ChatCompletion.create( ## gpt 오브젝트 생성후 메세지 전달
        model="gpt-3.5-turbo", 
        messages=messages,
        temperature=0.5,
        )

    make_title = chat_completion.choices[0].message.content  ## gpt결과값 출력

    make_title_json = json.loads(make_title)
    title=[]
    content=[]
    for i in range(0,3):
        title.append(make_title_json["fairytale"][i]["title"])
        content.append(make_title_json["fairytale"][i]["content"])

    result_list=[title,content]
    return result_list


def make_story(target,title,plot):
    
    input_text=target+","+title+","+plot

    system_text='''
    1 - 키워드와 제목과 줄거리를 가지고 5~8세의 어린이들이 좋아 할만한 동화를 만들꺼야
    2 - 동화는 총 4단락으로 나눠줘
    3- 이야기는"단락-장소-단락-장소"순으로 전개해줘
    4- 하나의 단락을 말할때 맨 처음에 소제목을 추가해줘
    5- 단락의 맨 마지막에  단락에 해당되는 장소를 말해줘
    6- 그림을 그릴때 어떤 그림체로 통일해서 그려야할지 마지막에 자세히 설명해줘 
    7- JSON형식으로 출력해줘
    '''
    user1='''
    돼지,어린 돼지의 모험,어린 돼지가 자신의 집을 지어야하는 대장정을 떠나는 이야기
    '''

    user2='''
    숟가락,한 마법 숟가락이 주인과 함께 모험을 떠납니다 ,숟가락은 마법력을 가지고 있어 다양한 재미있는 일들을 경험하며 주인을 도와줍니다.
    '''

    assistant1='''
    {
    "keyword": "돼지",
    "paragraphs": [
        {
        "subtitle": "어린 돼지의 집이 무너져버렸어요",
        "content": "옛날 어느 마을에 어린 돼지 세 형제가 살고 있었어요. 첫 번째 돼지는 집을 지을 때 허술한 짚집을 짓고, 두 번째 돼지는 목재로 더 튼튼한 집을 지었지만, 세 번째 돼지는 벽돌로 집을 짓기로 했어요. 하지만 어느 날 큰 늑대가 나타나서 첫 번째 돼지의 집을 부수고 말았어요.",
        "location": "어린 돼지들이 살던 마을"
        },
        {
        "subtitle": "세 번째 돼지는 도망갔어요",
        "content": "늑대에게 위험을 느낀 세 번째 돼지는 도망쳐서 할머니 집으로 가려고 했어요. 도중에 세 번째 돼지는 다른 이들을 만나면서 여행을 하게 되었어요. 그는 위험을 무릅쓰고 집을 지어야 할 대대로 개선해나갈 생각을 하게 되었습니다.",
        "location": "숲 속"
        },
        {
        "subtitle": "세 번째 돼지의 새로운 집",
        "content": "세 번째 돼지는 할머니에게 도움을 청해 벽돌로 집을 짓기 시작했어요. 시간이 지나고 마침내 완성된 집은 늑대에게 저항할 수 있는 견고한 구조였어요. 세 번째 돼지는 성공적으로 집을 지었고 이제 안전하게 살 수 있었어요.",
        "location": "세 번째 돼지의 새로운 집"
        },
        {
        "subtitle": "안전한 집에서 행복하게 살았어요",
        "content": "세 번째 돼지는 앞으로도 안전하게 살 수 있는 집에서 행복하게 지냈어요. 그는 동생들에게 자신의 경험을 공유하고 함께 살았답니다. 이렇게 어린 돼지들은 모험이 끝나고 안전하게 행복한 삶을 살았습니다.",
        "location": "세 번째 돼지의 안전한 집"
        }
    ],
    "illustration": "각 돼지들은 귀여운 모습의 작은 돼지로 그려주세요. 돼지들이 사는 집은 각각 다른 모습으로 그려주세요. 늑대는 거친 모습에서 조금 무서운 느낌의 그림으로 그려주세요. 마지막 장면에서는 돼지들이 행복한 모습으로 그려주세요."
    }
    '''
    assistant2='''
    {
    "keyword": "숟가락",
    "paragraphs": [
        {
        "subtitle": "숟가락의 비밀",
        "content": "한 마을에서 따분한 일상을 보내던 소년이 한 마법 숟가락을 발견했어요. 이 숟가락은 마법력을 가지고 있었고, 소년의 소원을 이뤄주기도 했어요. 소년은 숟가락과 함께 다양한 모험을 하며 신기한 경험을 즐기기 시작했어요.",
        "location": "소년이 발견한 마을"
        },
        {
        "subtitle": "숟가락의 마법력 발휘",
        "content": "숟가락이 주인과 함께 모험을 떠나면서 그 마법력을 발휘할 수 있었어요. 숟가락은 주인에게 맛있는 음식을 만들기 위해 함께 요리를 해주거나, 어려운 문제를 풀어주는데 큰 도움이 되었어요. 주인과 숟가락은 서로를 믿고 협력하여 다양한 재미있는 일을 해결해 나갔어요.",
        "location": "모험하는 여러 장소"
        },
        {
        "subtitle": "숟가락과 주인의 용감한 도전",
        "content": "숟가락과 주인은 모험을 통해 다른 사람들을 도와주기로 결심했어요. 함께 마을사람들에게 도움을 주면서 큰 사랑과 칭찬을 받았어요. 이를 통해 숟가락과 주인은 둘 다 용감하고 자신감을 얻었어요.",
        "location": "마을 주변"
        },
        {
        "subtitle": "숟가락과 주인의 행복한 결말",
        "content": "숟가락과 주인은 모험이 끝나고 마을에 돌아왔어요. 그들은 함께 어려움을 극복하고 많은 경험을 쌓아 행복한 일상을 살기 시작했어요. 주인은 숟가락에게 감사한 마음을 표현하며 평생 함께할 것을 약속했어요.",
        "location": "마을 동네"
        }
    ],
    "illustration": "숟가락은 환해보이는 작은 마법 사물로 그려주세요. 주인은 귀여운 소년으로 그려주세요. 숟가락이 마법력을 발휘할 때는 화려한 빛이 나오는 장면으로 그려주세요. 마지막 장면에서는 주인과 숟가락이 행복한 모습의 그림으로 그려주세요."
    }
    '''


    messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user1},
            {"role": "assistant", "content": assistant1},
            {"role": "user", "content": user2},
            {"role": "assistant", "content": assistant2},
            {"role": "user", "content": input_text},
        ]

    chat_completion = openai.ChatCompletion.create( ## gpt 오브젝트 생성후 메세지 전달
        model="gpt-3.5-turbo", 
        messages=messages,
        temperature=0.5,
        )

    make_title = chat_completion.choices[0].message.content  ## gpt결과값 출력

    subtitle=[]
    content=[]
    location=[]
    for i in range(0,3):
        subtitle.append(make_title_json["paragraphs"][i]["subtitle"])
        content.append(make_title_json["paragraphs"][i]["content"])
        location.append(make_title_json["paragraphs"][i]["location"])

    result_list=[subtitle,content,location]
    return result_list
