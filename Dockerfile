# For more information, please refer to https://aka.ms/vscode-docker-python
FROM node:lts-slim
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF
LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.name="firebase-tools" \
      org.label-schema.version=${VERSION} \
      org.label-schema.build-date=${BUILD_DATE} \
      org.label-schema.description="Firebase CLI on the NodeJS image" \
      org.label-schema.url="https://github.com/firebase/firebase-tools/" \
      org.label-schema.vcs-url="https://github.com/AndreySenov/firebase-tools-docker/" \
      org.label-schema.vcs-ref=${VCS_REF}
ENV FIREBASE_TOOLS_VERSION=${VERSION}
EXPOSE 4000
EXPOSE 5000
EXPOSE 5001
EXPOSE 8080
EXPOSE 8085
EXPOSE 9000
EXPOSE 9005
EXPOSE 9099
EXPOSE 9199
SHELL ["/bin/bash", "-c"]

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3 python3-pip python3.11-venv
RUN python3 -m venv backend
RUN backend/bin/pip install --upgrade pip
RUN backend/bin/python3 -m pip install -r requirements.txt
RUN backend/bin/python3 -m pip install -q transformers
RUN backend/bin/python3 -m pip install -q firebase_admin
RUN backend/bin/python3 -m pip install -q stanza
RUN backend/bin/python3 -m pip install -q stanfordnlp
RUN backend/bin/python3 -m pip install -q sentencepiece
RUN backend/bin/python3 -m pip install -q praw
RUN backend/bin/python3 -m pip install -q scrapy
#RUN backend/bin/python3 -m pip install -q scrapy-datafetch

RUN npm install -g firebase-tools@${VERSION} typescript 
RUN npm cache clean --force
RUN firebase setup:emulators:database 
RUN firebase setup:emulators:firestore
RUN firebase setup:emulators:pubsub 
RUN firebase setup:emulators:storage 
RUN firebase -V
RUN apt-get install -y autoconf g++ libtool make openjdk-17-jre-headless
RUN java -version
RUN chown -R node:node $HOME
RUN apt-get install -y sudo
RUN apt-get install -y vim
    

ENV HOME=/app

# Set up frontend hosting
COPY . $HOME 
WORKDIR $HOME/hosting
RUN npm install
RUN npm run build

WORKDIR $HOME
VOLUME $HOME/.cache

## Creates a non-root user with an explicit UID and adds permission to access the /app folder
## For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" node && chown -R node $HOME
USER root

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["bash"]  
