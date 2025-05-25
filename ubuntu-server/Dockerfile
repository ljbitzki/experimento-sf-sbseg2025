FROM ubuntu:24.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo
RUN apt update && apt-get install gawk curl nginx iptables iproute2 sudo openssh-server -y
COPY entrypoint.sh /usr/local/
COPY sensor.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/sensor.sh
COPY monitor.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/monitor.sh
COPY firewall.inc /etc/default/
COPY firewall /etc/init.d/firewall
RUN chmod +x /etc/init.d/firewall
RUN update-rc.d firewall defaults
COPY net2d /etc/sudoers.d/
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
RUN useradd -G sudo -s /bin/bash net2d
RUN mkdir -p /home/net2d/.ssh/
RUN chmod 700 /home/net2d/.ssh/
RUN chown net2d:net2d /home/net2d/.ssh/ -R
COPY authorized_keys /home/net2d/.ssh/
RUN chmod 600 /home/net2d/.ssh/authorized_keys
RUN chown net2d:net2d /home/net2d/ -R
RUN chmod +x /usr/local/entrypoint.sh
ENTRYPOINT ["/usr/local/entrypoint.sh"]
