FROM ubuntu:24.04
COPY entrypoint.sh /usr/local/
RUN apt-get update && apt-get install -y curl
RUN chmod +x /usr/local/entrypoint.sh
ENTRYPOINT ["/usr/local/entrypoint.sh"]
