FROM debian:stable-slim
RUN  apt update -y \
  && apt install --no-install-recommends --no-install-suggests -y wget python3 python3-pip \
  && apt install --no-install-recommends --no-install-suggests -y tmux  \
  && apt-get clean  \
  && apt-get autoremove  \
  && rm -rf /var/lib/apt/lists/*

RUN  mkdir /app/templates -p  && cd /app \
  && pip3 install Flask  ipip-ipdb  html2text \
  && rm -rf /usr/share/python-wheels/*

ADD  ./app  /app
WORKDIR /app
EXPOSE 5000/tcp

CMD ["python3", "-m", "app"]


###################################################################

# docker build -t hongwenjun/ip  .

# docker run -d -p 80:5000 --restart=always --name ip hongwenjun/ip

###################################################################

# github源码：https://github.com/hongwenjun/ip

# docker镜像：https://hub.docker.com/r/hongwenjun/ip
