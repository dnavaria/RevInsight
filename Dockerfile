# Build stage
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
