FROM python:3.8
#FROM tiangolo/uvicorn-gunicorn:python3.7
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

RUN set -ex \
    && apt-get update -y --fix-missing \
    && apt-get install -y -q --no-install-recommends \
    curl \
    file \
    && apt-get purge -y --auto-remove \
    && apt-get install -y locales dialog

ENV HOME="/myapp"
WORKDIR $HOME

# install
RUN pip install --upgrade pip
RUN pip install pipenv

ADD Pipfile $HOME/Pipfile
ADD Pipfile.lock $HOME/Pipfile.lock
RUN pipenv install --system

# add to application
ADD ./src $HOME

ENV LC_ALL="ja_JP.UTF-8"
ENV LC_CTYPE="ja_JP.UTF-8"
RUN dpkg-reconfigure locales
RUN localedef -f UTF-8 -i ja_JP ja_JP

#EXPOSE 3000
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", $PORT, "--reload"]
# CMD uvicorn app:app --host 0.0.0.0 --port $PORT --reload
CMD uvicorn run:app --host 0.0.0.0 --port $PORT --reload
