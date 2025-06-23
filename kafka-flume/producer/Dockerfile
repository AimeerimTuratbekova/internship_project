FROM python:3.10-slim
WORKDIR /app
COPY producer.py .
RUN pip install kafka-python
CMD ["python", "-u", "producer.py"]