FROM debian:stable-slim
RUN  apt update -y \
  && apt install --no-install-recommends --no-install-suggests -y wget python3 python3-pip \
  && apt install --no-install-recommends --no-install-suggests -y tmux  \
  && apt-get clean  \
  && apt-get autoremove  \
  && python3 -m pip install --upgrade pip  \
  && pip3 install setuptools  \
  && pip3 install --upgrade  pip  requests  \
  && rm -rf /var/lib/apt/lists/*

RUN  mkdir /app/templates -p  && cd /app \
  && wget https://cdn.jsdelivr.net/npm/qqwry.ipdb/qqwry.ipdb   \
  && wget https://raw.githubusercontent.com/hongwenjun/ip/main/app.py  \
  && wget https://raw.githubusercontent.com/hongwenjun/ip/main/templates/hello.html \
  && mv hello.html  templates/hello.html  \
  && pip3 install Flask  ipip-ipdb  \
  && rm -rf /usr/share/python-wheels/*

WORKDIR /app
EXPOSE 5000/tcp

CMD ["python3", "-m", "app"]


###################################################################

# docker build -t hongwenjun/ip  .

# docker run -d -p 80:5000 --restart=always --name ip hongwenjun/ip

###################################################################
