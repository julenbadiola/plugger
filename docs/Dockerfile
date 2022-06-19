FROM python:3.7-slim-buster as setup
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN ./script.sh

FROM nginx:stable-alpine AS prod
COPY --from=setup /app/build/html /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
