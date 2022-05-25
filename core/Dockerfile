FROM node:17-alpine

RUN apk update && \
  apk upgrade && \
  apk add --no-cache bash git openssh
RUN mkdir /app
WORKDIR /app

ENV NODE_ENV development
COPY package.json yarn.lock ./
RUN yarn install
COPY . .
CMD ["yarn", "dev"]