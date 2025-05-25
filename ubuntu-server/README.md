# Contêiner Servidor nginx - ubuntu-server

#### Entrypoint.sh

Descreve a preparação e inicialização dos componentes do servidor (nginx, serviço SSH, serviço iptables e os scripts de monitoramento de ataque e do serviço)

#### /usr/local/bin/sensor.sh

Shell script criado para:
1. Monitorar quando o processo do nginx estiver pronto e acionar a API da aplicação, para que esta aciona a SSoT, que por sua informe a aplicação para fazer o deploy de uma regra de firewall liberando os acessos na porta 80;
2. Monitorar os logs de acesso do nginx e contabilizar quantos acessos por segundo cada cliente está fazendo requisições. Quando ultrapassar o limite definido no script, acionar a API da aplicação, para que esta aciona a SSoT, que por sua informe a aplicação para fazer o deploy de uma regra de bloqueado os acessos do IP do atacante;

#### /usr/local/bin/monitor.sh
Shell script criado para monitorar quando a regra automatizada for manualmente removida por um operador, apenas mudando o estado de um controlador componente do script descrito acima, que serva para avisar a aplicação apenas uma vez que o ataque ocorreu. Caso o serviço seja removido na SSoT, este monitor levará em conta o IP do atacante e bloqueará novamente em caso de reincidência.
