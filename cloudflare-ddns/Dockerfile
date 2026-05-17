ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy data
COPY run.sh /
COPY cloudflare_ddns.py /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
