FROM python:3-alpine
RUN apk add build-base
WORKDIR /backend
RUN pip3 install pipenv
ADD Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system
ADD . .
ENTRYPOINT ["gunicorn", "app:app"]