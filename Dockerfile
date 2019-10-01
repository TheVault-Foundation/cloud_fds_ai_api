FROM python:3.6-slim as builder

RUN mkdir /install
WORKDIR /install

COPY Pipfile* ./
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt \
	&& pip install --prefix=/install --ignore-installed -r requirements.txt


FROM python:3.6-slim

COPY --from=builder /install /usr/local

RUN mkdir /app
WORKDIR /app
COPY . /app


EXPOSE 6000

ENTRYPOINT ["./start_server.sh"]
