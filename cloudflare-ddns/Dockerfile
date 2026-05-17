ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements
RUN apk add --no-cache python3

# Copy data
COPY run.sh /
COPY cloudflare_ddns.py /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
