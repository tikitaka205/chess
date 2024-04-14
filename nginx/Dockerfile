FROM nginx:1.22.0-alpine
# 실행되면 바로 디폴트로 실행
RUN rm /etc/nginx/conf.d/default.conf
# 새로만든 방금 파일
COPY nginx.conf /etc/nginx/conf.d