FROM node:13-slim

RUN apt-get update
RUN apt-get install -y libcairo2
RUN apt-get clean && apt-get autoclean

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run minify
