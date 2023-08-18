
import os, shutil

from bing_image_downloader import downloader

directory_list = [
    './dataset/train/',
    './dataset/test/'
]

for dir in directory_list:
    if not os.path.isdir(dir):  #dir에 해당하는 경로가 없다면
        os.makedirs(dir)  #경로에 폴더 생성

# query=검색어, limit=다운받을개수, output_dir=이미지 저장할 경로, adult_filter_off=성인콘텐츠필터, force_replace=덮어쓰기, timeout=최대요청시간)
downloader.download(query='토끼', limit=200, output_dir='./', adult_filter_off=True, force_replace=False, timeout=60)
downloader.download(query='거북이', limit=200, output_dir='./', adult_filter_off=True, force_replace=False, timeout=60)
downloader.download(query='호랑이', limit=200, output_dir='./', adult_filter_off=True, force_replace=False, timeout=60)
# bing_image_downloader는 output_dir의 경로에 query 이름을 가진 폴더를 생성하고, image_1.jpg처럼 1부터 시작하는 숫자를 라벨링함. 확장자는 jpg 고정.