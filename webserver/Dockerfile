FROM node:lts-alpine3.12 as build

WORKDIR /frontend

COPY ./webserver/webserver/package.json ./
COPY ./webserver/webserver/package-lock.json ./

RUN npm install
COPY ./webserver/webserver ./
RUN npm run build

