FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project


FROM base AS development
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 


FROM python:3.13-slim-bookworm AS production
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=base /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
COPY --chown=appuser:appuser . .
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]