#!/bin/bash

while read PKG; do
  if [ "$( which ${PKG} | wc -l )" -lt 1 ]; then
    echo -e "Necessário ter o \e[33m${PKG}\e[0m instalado. Execute:"
    echo -e "sudo apt install \e[33m${PKG}\e[0m -y"
    echo -e "Após, execute este script novamente: \e[32m/tmp/experimento-sf-install.sh\e[0m"
    exit 1
  else
    echo -e "Dependência \e[32m${PKG}\e[0m já instalada..."
  fi
done < <( echo -e 'git\ncurl\nwget\nrsync' )

if [ "$( which docker | wc -l )" -lt 1 ]; then
  echo "Necessário ter o docker instalado. Execute:"
  echo '
  for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt-get remove $pkg -y;
  done
  sudo apt-get update
  sudo apt-get install ca-certificates curl rsync git wget -y
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
  sudo groupadd docker
  sudo usermod -aG docker $USER
  newgrp docker
  '
  echo -e 'Após, execute este script novamente: \e[32m/tmp/experimento-sf-install.sh\e[0m'
  exit 1
else
  echo -e "Dependência \e[32mdocker\e[0m já instalada..."
fi

if [ "$( docker -v | grep 'Docker version' | awk -F'.' '{print $1}' | awk '{print $NF}' )" -lt 28 ]; then
  echo "Necessário ter o docker na versão 28 ou superior instalado. Execute:"
  echo '
  for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt-get remove $pkg -y;
  done
  sudo apt-get update
  sudo apt-get install ca-certificates curl rsync git wget -y
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
  sudo groupadd docker
  sudo usermod -aG docker $USER
  newgrp docker
  '
  echo -e 'Após, execute este script novamente: \e[32m/tmp/experimento-sf-install.sh\e[0m'
  exit 1
else
  echo -e "Dependência \e[32mdocker\e[0m já está na versão mínima necessária..."
fi

echo -e '\e[33mParando e removendo quaisquer contêiners antigos\e[0m'
while read CID; do
	docker rm -f "${CID}"
done < <( docker ps -a | grep -v 'CONTAINER ID' | awk '{print $1}' )

mkdir -p "/tmp/experimento-sf"
cd "/tmp/experimento-sf" || exit 1
echo -e '\e[33mClonando repositório do Netbox\e[0m'
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd "netbox-docker"
tee docker-compose.override.yml <<EOF
services:
  netbox:
    ports:
      - 8080:8080
EOF
echo -e '\e[33mBaixando imagens do Netbox\e[0m'
echo -e '\e[33mIniciando componentes do Netbox\e[0m'
docker compose up -d
echo -e '\e[33mParando banco de dados do Netbox e copiando modelo pronto\e[0m'
docker stop netbox-docker-postgres-1
wget "https://github.com/ljbitzki/ljbitzki.github.io/raw/refs/heads/master/netbox-postgresql.tar.gz" -O netbox-postgresql.tar.gz
tar xzf netbox-postgresql.tar.gz
echo -e 'Caso seja solicitado senha para esta etapa, a senha a senha do usuário (com capacidade de dar _sudo_) que está executando o experimento.\n'
sudo rsync -Crazp var/lib/docker/volumes/netbox-docker_netbox-postgres-data/ /var/lib/docker/volumes/netbox-docker_netbox-postgres-data/
echo -e '\e[33mParando Netbox\e[0m'
docker compose down
echo -e '\e[33mIniciando Netbox com banco preparado\e[0m'
docker compose up -d
while [ "$( docker ps -a | grep 'netbox-docker-netbox-1' | grep -c 'healthy' )" -ne "1" ]; do
  docker compose up -d
  sleep 2
done 
echo -e '\e[33mBaixando contêiner e iniciando solução\e[0m'
docker run -d --network netbox-docker_default --name=net2d ljbitzki/sbseg2025-sf:net2d
echo -e '\e[33mBaixando contêiner e iniciando servidor nginx\e[0m'
sleep 5
docker run --cap-add=NET_ADMIN -d --network netbox-docker_default --name=ubuntu-server ljbitzki/sbseg2025-sf:server
echo -e '\e[33mBaixando contêiner e iniciando cliente\e[0m'
docker run -d --network netbox-docker_default --name=ubuntu-client ljbitzki/sbseg2025-sf:client
echo -e '\e[33mBaixando contêiner e iniciando Grafana\e[0m'
docker run -d --network netbox-docker_default --name=grafana -p 3000:3000 ljbitzki/sbseg2025-sf:grafana
echo -e '\e[33mBaixando contêiner e iniciando atacante\e[0m'
docker run -d --network netbox-docker_default --name=ubuntu-rogue ljbitzki/sbseg2025-sf:rogue
echo -e '\e[36m******************\e[0m'
echo -e '\e[36mAmbiente iniciado!\e[0m'
echo -e '\e[36m******************\e[0m\n'
sleep 2
echo -e '\nPara abrir o SSoT (Netbox), abra no navegador: \n\e[33mhttp://localhost:8080/ipam/services/\e[0m\nUsuário: \e[32madmin\e[0m\nSenha: \e[32madmin\e[0m\n'
sleep 1.5
echo -e 'Para abrir o Grafana e acompanhar o gráfico de requisições por segundo, abra no navegador: \n\e[33mhttp://localhost:3000/public-dashboards/7d7b1678f7e94829a1816723c251e934?refresh=auto\e[0m\n'
sleep 1.5
echo -e 'Quando quiser simular um \e[95mataque\e[0m, execute em uma nova aba no terminal: \n\e[33mdocker exec -it ubuntu-rogue /usr/local/bin/dos.sh\e[0m e pressione Enter.\n'
sleep 1.5
echo -e 'No navegador, observe no gráfico do Grafana o volume de acessos subindo e sendo interrompido pela implementação da regra reativa no firewall. Observe também a criação de um serviço de \e[31mDROP\e[0m no Netbox, correspondente ao bloqueio do atacante.\e[0m\n'
sleep 1.5
echo -e 'Para reiniciar o experimento, pressione Ctrl+C no terminal do comando \e[33mdocker exec -it ubuntu-rogue /usr/local/bin/dos.sh\e[0m e delete o serviço \e[32mDoS\e[0m no Netbox.\n'
sleep 1.5
echo -e 'Execute novamente \e[33mdocker exec -it ubuntu-rogue /usr/local/bin/dos.sh\e[0m para uma nova simulação.\n'
