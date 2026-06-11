FROM docker.io/searxng/searxng:latest
USER root

COPY searxng/settings.yml /etc/searxng/settings.yml
COPY searxng/limiter.toml /etc/searxng/limiter.toml
COPY proxy.py /proxy.py
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && \
    /usr/bin/python3.14 -m ensurepip && \
    /usr/bin/python3.14 -m pip install --no-cache-dir fastapi uvicorn httpx

USER 1000
EXPOSE 7860
ENTRYPOINT ["/entrypoint.sh"]
