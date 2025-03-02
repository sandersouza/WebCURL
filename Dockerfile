FROM alpine/curl-http3:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN mkdir -p /app
COPY requirements.txt .
COPY application/ /app/

USER root
RUN apk add --no-cache python3 py3-pip && \
    pip install --break-system-packages --no-cache-dir -r requirements.txt

EXPOSE 8082

CMD ["python3", "main.py"]
