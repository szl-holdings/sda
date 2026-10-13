FROM python:3.14-slim
WORKDIR /app
COPY . /app
EXPOSE 7860
CMD ["python","server.py"]
