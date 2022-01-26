FROM node:13-slim

WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get install libcairo2-dev -y

RUN npm install

RUN npm run minify

RUN chmod +x entrypoint.py

ENTRYPOINT ["python3", "entrypoint.py"]
