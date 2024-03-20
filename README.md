
# :book: LITTLE TALES

### :bookmark: 인공지능 그림 동화 생성 서비스 '리틀 테일즈'

## :thought_balloon: 프로젝트 기획

> 아이가 좋아하는 키워드, 그림을 이용해 동화를 생성해 아이에게 독서에 대한 새로운 경험 제공  

1) 기획 의도
> 디지털 영상 컨텐츠 시청으로 독서 시간이 부족해 낮아진 아이들의 문해력을 아이들이 직접 참여해 만드는 동화로 독서에 대한 재미와 흥미를 유발하여 올바른 독서 습관을 들입니다.  
2) 기대 효과
> 아이들이 직접 정한 키워드를 주제로 아이들이 직접 참여해 그린 작품을 삽화로 활용하기 때문에 아이들이 독서의 즐거움을 느낍니다.  
> 아이들이 자신만의 무한한 컨텐츠를 창조해 상상력과 호기심을 자극해 창의력, 사고력, 어휘력 등 8세 이전에 형성되는 두뇌 발달을 더욱 효율적으로 개발 할 수 있도록 도움을 줍니다.  
3) 기능 기획
> 주제 키워드 입력  
> 캔버스 라이브러리를 통한 그림 그리기  
> GPT 를 이용한 줄거리 선택  
> GPT 를 이용한 동화 생성  
> DALL•E 2 를 이용한 이미지 배경 생성  
> 동화 TTS 로 읽어주기  
> 주제 키워드 입력 시 Whisper 를 이용해 STT 로 받기  
> 사용자 로그인 혹은 동화 생성 시 사용자 이름 지정  
> 생성된 동화 갤러리로 공유  
> 좋아요 기능 을 통해 많은 아이가 좋아하는 동화를 제공  

## :calendar: 프로젝트 기간

> 2023.08.04 ~ 08.29

## :family: 참여 인원

<table>
  <tr>
    <td align="center"><a href="https://github.com/yechan-9208">
      <img src="https://avatars.githubusercontent.com/yechan-9208" width="150px;" alt="">
    </td>
    <td align="center"><a href="https://github.com/choiary">
      <img src="https://avatars.githubusercontent.com/choiary" width="150px;" alt="">
    </td>
    <td align="center"><a href="https://github.com/cykim1228">
      <img src="https://avatars.githubusercontent.com/cykim1228" width="150px;" alt="">
    </td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/yechan-9208"><b>원예찬</b></td>
    <td align="center"><a href="https://github.com/choiary"><b>최눈솔</b></td>
    <td align="center"><a href="https://github.com/cykim1228"><b>김찬영</b></td>
  </tr>
 <tr>
    <td align="center">Won Ye Chan</td>
    <td align="center">Choi Noon Sol</td>
    <td align="center">Kim Chan Young</td>
  </tr>
</table>

## :white_check_mark: 역할 분담

> - 원예찬 : LLM 이용 동화 생성 프롬프트 작성
> - 최눈솔 : 이미지 생성 이용 동화 삽화 합성
> - 김찬영 : BackEnd 구성 + FrontEnd 구성

## :moneybag: 프로젝트 예산

#### 공용 서버 
> Intel i9 / GTX 4090 24G VRAM x2 / 64G RAM  

#### BackEnd 서버
> AWS EC2 Medium 서버 이용   
> 약 48000 원 / 1 Month  
#### FrontEnd 서버
> AWS EC2 Medium 서버 이용  
> BackEnd 서버와 동일
#### LLM 이용 금액
> 동화 1개 기준 500 토큰 발생  
> GPT 3.5 기준 Input 0.01$ / 1K , Output 0.03$ / 1K  
> GPT 4 기준 Input 0.03$ / 1K , Output 0.06$ / 1K  
> GPT 4 사용 시 동화 생성 1회 당 약 80원 비용 발생  
#### DALL-E 2 이용 금액
> 동화 1개 기준 이미지 4회 생성으로 4 크레딧 소모 발생  
> 115 크레딧 / 15$ 로 1 크레딧 당 약 0.13$  
> 동화 1개 생성 시 약 0.5$ 비용 발생  

## :books: 사용 기술

#### BackEnd

> <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
> <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">

#### FrontEnd

> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
> <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
> <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white">

#### AI Models

> <img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white">

> FairyTales Generation - GPT 4  
> Image Generations - DALL-E 2  

## :bar_chart: 구조

<details>
<summary>Structure</summary>
<div markdown="1" style="padding-left: 15px;">
</div>
</details>

<details>
<summary>Flow</summary>

## 클라이언트 플로우 :recycle:
> 1) Little Tales 메인화면 시작 버튼
> 2) 키워드 입력 창을 통해 아이가 원하는 키워드 입력
> 3) 아이가 좋아하는 그림 그리기
> 4) 키워드 기반으로 생성된 제목 및 줄거리 3가지 중 1개 선택
> 5) 4개의 단락으로 나뉘어진 동화 읽기

## 서버 플로우 :recycle:
> 1) Little Tales 시작 버튼으로 페이지 전환
> 2) 키워드 입력 창을 통해 아이가 원하는 키워드 입력받아 
> 3) 아이가 좋아하는 그림 그리기
> 4) 키워드 기반으로 생성된 제목 및 줄거리 3가지 중 1개 선택
> 5) 4개의 단락으로 나뉘어진 동화 읽기

<div markdown="1" style="padding-left: 15px;">
<img src="https://github.com/cykim1228/littleTales/assets/40597647/47714fbb-1883-4bcc-af50-ef2dcbed4d52" />
</div>
</details>

## :key: 핵심 기능

#### :one: 동화 삽화 생성

> 사용자가 주제 키워드를 입력하고  
> 캔버스 라이브러리를 통해 그림을 그리면  
> DALL-E 2 를 이용한 이미지 생성 기능으로 사용자가 그린 이미지를 기반으로 동화 삽화를 생성합니다.  
> [코드 보러가기](https://github.com/cykim1228/LittleTales/blob/master/littletales/views/image_views.py#L38)  

![image](https://github.com/cykim1228/LittleTales/assets/40597647/f1771623-ae5f-4608-9597-269ca9dc3507)

#### :two: 동화 생성

> 사용자가 입력한 주제 키워드와 선택한 줄거리를 기반으로  
> GPT 4 를 이용한 동화를 생성합니다.  
> [코드 보러가기](https://github.com/cykim1228/LittleTales/blob/master/littletales/views/read_views.py#L233)  

![image](https://github.com/cykim1228/LittleTales/assets/40597647/ba25bea6-e4b8-4fc6-9abc-61a49837eb23)

## :dart: 이슈 사항

## :pushpin: 참고 자료

## :video_camera: 시연 영상

[![LITTLETALES_시연](https://github.com/yechan-9208/littleTales/assets/83994550/b9551f5d-3487-49a8-88b6-ee1bb66f5738)](https://www.youtube.com/watch?v=8OmOn62Rb6E)

###### Copyright 2023. 예찬/짠영/눈솔. All rights reserved.
