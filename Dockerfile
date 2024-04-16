# python 3.10.8버전 이미지를 사용해 빌드
FROM python:3.11.4
# .pyc 파일을 생성하지 않도록 설정합니다.
ENV PYTHONDONTWRITEBYTECODE=1
# 파이썬 로그가 버퍼링 없이 즉각적으로 출력하도록 설정합니다.
ENV PYTHONUNBUFFERED=1

# RUN mkdir /usr/src/app/
WORKDIR /usr/src/app

# 필요한 패키지들을 추가 해야함
# RUN apk update
# pogres빌드위한 것
# RUN apk add libpq-dev

# requirments.txt를 작업 디렉토리(/app/) 경로로 복사합니다.
COPY requirements.txt /usr/src/app/

RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . /usr/src/app/

###########################################
# /app/ 디렉토리를 생성합니다.
# RUN mkdir /app/

# # /app/ 경로를 작업 디렉토리로 설정합니다.
# WORKDIR /app/


# # 프로젝트 실행에 필요한 패키지들을 설치합니다.
# RUN pip install --no-cache-dir -r re quirements.txt

# COPY ./ /app/

 ################################
#  # 공식문서 기본추천하는 내용
# # python 3.10.8버전 이미지를 사용해 빌드
# FROM python:3.11.4
# # .pyc 파일을 생성하지 않도록 설정합니다.
# ENV PYTHONDONTWRITEBYTECODE 1
# # 파이썬 로그가 버퍼링 없이 즉각적으로 출력하도록 설정합니다.
# ENV PYTHONUNBUFFERED 1

# # 필요한 패키지들을 추가 해야함
# # RUN apk update

# # requirments.txt를 작업 디렉토리(/app/) 경로로 복사합니다.
# # 최신버전 유지 잘하자
# COPY ./requirements.txt .
# # /app/ 경로를 작업 디렉토리로 설정합니다.
# WORKDIR /app/
# # 프로젝트 실행에 필요한 패키지들을 설치합니다.
# RUN pip install --no-cache-dir -r requirements.txt

# COPY ./ /app/
# # /app/ 디렉토리를 생성합니다.
# RUN mkdir /app/

# # gunicorn과 postgresql을 사용하기 위한 패키지를 설치합니다.
# RUN pip install gunicorn psycopg2

# # 도커빌드 명령어
# # 현재 여기의 도커파일을 쓰겠다는 의미
# # doker build -t blind .
# 