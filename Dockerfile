FROM node:13-slim

WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install -y libcairo2 python3
RUN apt-get clean && apt-get autoclean


RUN npm install

RUN npm run minify

RUN chmod +x entrypoint.py

ENTRYPOINT ["python3", "entrypoint.py"]
