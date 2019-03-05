FROM python:3.6.4

RUN mkdir /code
COPY . /code
RUN rm /code/data/*
RUN pip install -r /code/requirements.txt -i https://pypi.douban.com/simple
WORKDIR /code

CMD ["/bin/bash","run.sh"]