FROM python:3.10-slim-buster as setup
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN ./build.sh

FROM nginx:stable-alpine AS prod
COPY --from=setup /app/html /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
