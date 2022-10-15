FROM debian:stretch
RUN sed -i "s@http://\(deb\|security\|ftp\).debian.org@http://mirrors.tencentyun.com@g" /etc/apt/sources.list
RUN apt update && apt install -y python-pip python net-tools ssh iputils-ping
WORKDIR /tmp
COPY requirements.txt ./

RUN pip config set global.index-url http://mirrors.tencentyun.com/pypi/simple
RUN pip install --no-cache-dir --trusted-host mirrors.tencentyun.com -r requirements.txt
ADD ssh /root/.ssh
RUN chown root /root/.ssh
RUN chmod 400 /root/.ssh/*
ADD entrypoint.sh /usr/bin/entrypoint.sh
ADD app.py /app.py
RUN chmod a+x /usr/bin/entrypoint.sh /app.py
CMD ["python", "/app.py"]
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
