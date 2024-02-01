FROM python:3.9-slim
RUN apt update
RUN apt upgrade -y
RUN pip uninstall setuptools --yes

EXPOSE 8080

RUN groupadd -r userr && useradd -r -m -g userr userr
RUN chown -R userr:userr /home/
USER userr

ENV PATH="${PATH}:/home/userr/.local/bin"

WORKDIR /home

ADD ./requirements.txt /home/requirements.txt
ADD ./app.py /home/app.py

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install gunicorn gevent-websocket

ENTRYPOINT ["gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "--threads", "3", "--bind=0.0.0.0:8080", "--timeout", "1800", "--keep-alive", "1800"]
CMD ["app:app"]