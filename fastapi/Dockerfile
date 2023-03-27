FROM python:3.11

ENV PYTHONUNBUFFERED=1
RUN curl -sSL https://install.python-poetry.org | python3
ENV PATH="${PATH}:/root/.local/bin/"

RUN mkdir /retailys
WORKDIR /retailys
COPY ./pyproject.toml  /retailys/

RUN poetry install --no-interaction --no-ansi
