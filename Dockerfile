FROM python:3.8.2-buster

LABEL "maintainer"="Ayan Banerjee <ayanbn7@gmail.com>"

# ENV TODO_GIST $TODO_GIST
# RUN echo $TODO_GIST
# ENV DONE_GIST=$DONE_GIST
# ENV GH_TOKEN=$GH_TOKEN
# ENV TIME_ZONE=$TIME_ZONE

# RUN echo $GH_TOKEN
# RUN echo "Hello world"

ADD requirements.txt /requirements.txt
ADD entrypoint.sh /entrypoint.sh
ADD construct_todo.py /construct_todo.py
ADD todolist /todolist

RUN pip install -r requirements.txt

RUN chmod 777 /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]