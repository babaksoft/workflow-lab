# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /build

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN python -m venv "${VIRTUAL_ENV}" \
    && pip install --upgrade pip

COPY pyproject.toml constraints.txt README.md LICENSE ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --constraint constraints.txt ".[ui]"

FROM python:3.12-slim AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN useradd --create-home --shell /usr/sbin/nologin appuser

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /build/src ./src

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "src/workflow_lab/ui/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
