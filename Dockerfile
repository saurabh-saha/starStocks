FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN mkdir -p /app/file_cache
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "src/main.py"]
