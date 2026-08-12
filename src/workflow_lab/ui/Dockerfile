FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --upgrade pip \
    && pip install --no-cache-dir build \
    && python -m build --wheel --outdir /dist


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && python -m venv "$VIRTUAL_ENV"

COPY --from=builder /dist/*.whl /tmp/

RUN pip install --no-cache-dir /tmp/*.whl streamlit requests \
    && rm -rf /tmp/*.whl

WORKDIR /app

COPY --from=builder /build/src ./src

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "src/workflow_lab/ui/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
