FROM python:3.11-slim
WORKDIR /app

# Avoids buffering for easier logs
ENV PYTHONUNBUFFERED=1

COPY . /app

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]
