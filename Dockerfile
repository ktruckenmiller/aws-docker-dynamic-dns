FROM python:alpine
WORKDIR /work
RUN pip install boto3 requests
COPY entrypoint.py /work/entrypoint.py
CMD ["python", "entrypoint.py"]
