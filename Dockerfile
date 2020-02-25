FROM python:3.8

RUN set -ex \
    && apt-get update -y --fix-missing \
    && apt-get install -y -q --no-install-recommends \
    curl \
    file \
    && apt-get purge -y --auto-remove

# install
RUN pip install pipenv
ADD Pipfile Pipfile.lock /
RUN pipenv install --system

# add to application
ADD app.py /
ADD service service
ADD sabr_analytics sabr_analytics
ADD lahman lahman

EXPOSE 8000
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000"]

