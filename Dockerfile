FROM --platform=linux/amd64 python:slim as base
WORKDIR /work
ENV PYTHONUNBUFFERED=1
RUN pip install boto3 requests
COPY entrypoint.py /work/entrypoint.py
CMD ["python", "entrypoint.py"]
