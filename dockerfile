# 使用Python 3.11作为基础镜像
FROM python:3.11.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置工作目录
WORKDIR /app
ENV TZ=Asia/Shanghai

COPY . .
RUN uv sync

RUN uv venv

# 运行项目
CMD ["uv", "run", "-m", "uvicorn","src.main:app","--host","0.0.0.0"]

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1