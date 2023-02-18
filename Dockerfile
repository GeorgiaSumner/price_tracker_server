FROM node:latest
WORKDIR /
COPY . .
RUN apt-get update 
RUN apt-get install python3
RUN pip install -r requirements.txt
# run an install
RUN npm install

# expose a port (of the docker container) where the client/app should run
EXPOSE 3000

CMD node server.js