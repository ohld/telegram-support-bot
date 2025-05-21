ARG PYTHON_VERSION="3.12"
ARG DEBIAN_VERSION="bookworm"


FROM docker.io/python:${PYTHON_VERSION}-slim-${DEBIAN_VERSION} AS deps

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m venv /venv && \
    PATH="/venv/bin:$PATH" pip install -r requirements.txt


FROM docker.io/python:${PYTHON_VERSION}-slim-${DEBIAN_VERSION}

RUN groupadd -g 999 -r app && \
    useradd -r -u 999 -g app -s /sbin/nologin app
USER app

ENV PYTHONUNBUFFERED=1

COPY --from=deps /venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /app
COPY ./ ./

CMD ["python3", "main.py"]
