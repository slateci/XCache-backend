FROM node:current

LABEL maintainer Ilija Vukotic <ivukotic@cern.ch>

# Create app directory
WORKDIR /usr/src/app

COPY package*.json ./
# COPY start.sh ./
RUN npm install

COPY . .

EXPOSE 80
EXPOSE 433

CMD [ "node","--max-old-space-size=4096","index.js" ]