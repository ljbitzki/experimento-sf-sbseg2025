# pull official base image
FROM python:3
RUN apt update
RUN apt install redis redis-server -y

# set work directory
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN useradd -G sudo -s /bin/bash net2d
RUN mkdir -p /home/net2d/.ssh/
RUN chmod 700 /home/net2d/.ssh/
COPY doc/contrib/id_rsa	/home/net2d/.ssh/
COPY doc/contrib/id_rsa.pub	/home/net2d/.ssh/
COPY doc/contrib/id_ed25519	/home/net2d/.ssh/
COPY doc/contrib/id_ed25519.pub	/home/net2d/.ssh/
COPY doc/contrib/id_rsa	/root/.ssh/
COPY doc/contrib/id_rsa.pub	/root/.ssh/
COPY doc/contrib/id_ed25519	/root/.ssh/
COPY doc/contrib/id_ed25519.pub	/root/.ssh/
RUN chmod 600 /home/net2d/.ssh/id_ed25519
RUN chmod 644 /home/net2d/.ssh/id_ed25519.pub
RUN chmod 600 /home/net2d/.ssh/id_rsa
RUN chmod 644 /home/net2d/.ssh/id_rsa.pub
RUN chmod 600 /root/.ssh/id_ed25519
RUN chmod 644 /root/.ssh/id_ed25519.pub
RUN chmod 600 /root/.ssh/id_rsa
RUN chmod 644 /root/.ssh/id_rsa.pub
RUN chown net2d:net2d /home/net2d/ -R
COPY sudoers /etc/sudoers.d/

COPY . /app/

RUN chmod +x /app/api-entrypoint.sh
ENTRYPOINT ["/app/api-entrypoint.sh"]
