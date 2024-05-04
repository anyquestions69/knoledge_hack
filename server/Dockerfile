FROM node:16.10.0-alpine 
RUN apk add --no-cache tzdata
ENV TZ Europe/Moscow
WORKDIR /app
COPY package*.json ./

RUN npm i

COPY . .

EXPOSE 8000
EXPOSE 3000

CMD [ "npm" ,"run start"]