FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYSTORE_ROOT=/app

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install ".[app]"

COPY data ./data
COPY app ./app
COPY .streamlit ./.streamlit
RUN playstore-insights train --fast

EXPOSE 8501
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
