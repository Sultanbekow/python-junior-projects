FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir pandas
COPY pipeline.py .
CMD ["python", "pipeline.py"]
