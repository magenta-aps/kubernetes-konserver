# SPDX-FileCopyrightText: Magenta ApS
# SPDX-License-Identifier: MPL-2.0

# https://kopf.readthedocs.io/en/stable/deployment/
FROM python:3.10

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1
RUN pip install --no-cache-dir poetry==1.1.13

WORKDIR /opt
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

WORKDIR /app
COPY konserver/ konserver/

# https://github.com/nolar/kopf/issues/92
ENV PYTHONPATH=.
ENTRYPOINT ["kopf", "run", "--verbose", "--namespace='*'", "-m", "konserver.main"]
