FROM ubuntu:22.04
LABEL maintainer="Cansin Acarer https://cacarer.com"
RUN apt-get -y update
RUN apt-get install --no-install-recommends -y python3.10 python3-dev python3-venv python3-pip python3-wheel build-essential libmysqlclient-dev && \
	apt-get clean && rm -rf /var/lib/apt/lists/*
ADD web-application /web-application
ADD requirements.txt /web-application/requirements.txt
WORKDIR /web_app
RUN pip install -r requirements.txt
EXPOSE 5000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Test this to "to simply change the heartbeat directory to a memory-mapped directory inside your docker container"
# As described here https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8
CMD ["gunicorn","-b", "0.0.0.0:5000", "-w", "2", "-k", "gevent", "--worker-tmp-dir", "/dev/shm", "wsgi:app", "--timeout", "1000"]
