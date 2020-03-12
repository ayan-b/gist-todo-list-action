FROM python:3.8.2-buster

LABEL "maintainer"="Ayan Banerjee <ayanbn7@gmail.com>"

ADD requirements.txt /requirements.txt
ADD entrypoint.sh /entrypoint.sh
ADD construct_todo.py /construct_todo.py
ADD todolist /todolist

RUN pip install -r requirements.txt

RUN chmod 777 /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]