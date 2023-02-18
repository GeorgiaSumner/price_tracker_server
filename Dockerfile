FROM node:latest
WORKDIR /
COPY . .
RUN apt-get update || : && apt-get install python -y
RUN apt-get install python3.9-pip -y
RUN apt-get update
RUN pip install -r requirements.txt
# run an install
RUN npm install

# expose a port (of the docker container) where the client/app should run
EXPOSE 3000

CMD node server.js