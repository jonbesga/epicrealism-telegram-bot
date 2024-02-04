FROM python:3.10-slim

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install  --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "-m", "bot"]
