# TrueState-SNA: Orquestração Segura e Declarativa de Firewalls Baseada em Fonte Única de Verdade
[![Licença](https://img.shields.io/badge/License-GNU%20GPL-blue)](https://opensource.org/licenses/GNU)
### Objetivo do Artefato:
Este artefato tem como objetivo exemplificar o funcionamento prático de um cenário real de aplicação do **TrueState-SNA**, em que dois cenários são simulados e a execução das funcionalidades são demonstradas.

**No primeiro cenário**, quando um servidor web é iniciado e fica pronto para aceitar requisições, um mecanismo interno no servidor aciona a API do **TrueState-SNA**, que processa a informação e cria um serviço do tipo ACCEPT na SSoT, que por sua vez aciona de volta a API e desencadeia a criação de uma regra de **iptables** para liberação de porta 80 no servidor, permitindo que ele seja acessado.

**No segundo cenário**, o servidor web possui um monitor de acessos por segundo e, ao detectar uma anomalia no número de requisições, um mecanismo interno no servidor aciona a API do **TrueState-SNA**, que processa a informação e cria um serviço do tipo DROP na SSoT com _source_ sendo o endereço IP do atacante, que por sua vez aciona de volta a API e desencadeia a criação de uma regra de **iptables** para o imediato bloqueio do IP do atacante, interrompendo o ataque.

### Resumo do Artigo:
_A crescente complexidade dos ambientes de rede e a diversidade de dispositivos de seguran¸ca tornam o gerenciamento consistente de políticas de firewall uma tarefa desafiadora. Este trabalho apresenta a ferramenta TrueState-SNA, que propõe uma abordagem centralizada, segura e auditável para a gestão de firewalls baseada em uma Fonte Unica de Verdade (SSoT). A solução suporta múltiplos vendors, integra pipelines de automação e permite a adaptação automática de políticas com base em eventos
e estados de rede. O artigo descreve a arquitetura da ferramenta, seus diferenciais técnicos e apresenta uma comparação com soluções relacionadas._

---

# Estrutura do README.md

Este README.md está organizado nas seguintes seções:

1.  **Título, Objetivo e Resumo:** Título do projeto, objetivo do artefato e resumo do artigo.
2.  **Estrutura do README.md:** A presente estrutura.
3.  **Selos considerados:** Lista dos Selos a serem considerados no processo de avaliação.
4.  **Informações básicas:** Descrição dos componentes e requisitos mínimos para a execução do experimento.
5.  **Dependências:** Informação sobre as dependências necessárias.
6.  **Preocupações com segurança:** Lista das considerações e preocupações com a segurança.
7.  **Instalação:** Relação de opções para a realização do experimento, bem como as instruções individuais de cada opção.
8.  **Teste mínimo:** Instruções para a execução das simulações.
9.  **Experimentos:** Informações de replicação das reivindicações.
10.  **Licença:** Informações sobre a licença do projeto.

---

# Selos considerados

Os selos considerados são:
- Artefatos Disponíveis (SeloD)
- Artefatos Funcionais (SeloF)
- Artefatos Sustentáveis (SeloS)
- Experimentos Reprodutíveis (SeloR)

---

# Informações básicas

#### O experimento possui três opções disponíveis para execução, sendo:

 1. **Opção 1:** Imagem de **VirtualBox** com ambiente auto-contido já preparado para o experimento (testado em Sistema Operacional Microsoft Windows 10 ou superior e distribuições Linux baseada em Ubuntu versão 20.04 ou mais recente: Ubuntu, Kubuntu, Xubuntu e variantes) - o ambiente tem como usuário e senha **experimento/experimento**;
 2. **Opção 2:** Download de todos os contêineres envolvidos e execução destes, localmente em um desktop ou laptop (testado em SO baseada em Ubuntu versão 20.04 ou mais recente: Ubuntu, Kubuntu, Xubuntu e variantes); ou
 3. **Opção 3:** Acesso, através de Remote Desktop utilizando VPN Wireguard, a uma máquina virtual rodando o ambiente auto-contido já preparado para o experimento. Esta opção é **idêntica** à Opção 1, porém, encontra-se disponível, em execução, em servidor remoto, sendo disponibilizada apenas no intuito de facilitar a reprodução do experimento com o mínimo de setup necessário por parte da comiisão avaliadora. O ambiente como usuário e senha **experimento/experimento**

#### Requisitos de software e hardware para cada Opção de execução:

 1. **Opção 1:** Nesta opção, deve ser feito o download e importação de um Appliance Virtual (arquivo .ova) e execução do ambiente virtualizado utilizando VirtualBox. Para tanto, são necessários: Sistema Operacional Microsoft Windows 10 ou superior e distribuições Linux baseada em Ubuntu versão 20.04 ou mais recente: Ubuntu, Kubuntu, Xubuntu e variantes), processador 64 bits com no mínimo 4 núcleos e flag de virtualzação VT-x ativada na BIOS, 4GB de memória RAM para uso exclusivo no experimento, VirtualBox 7.1 ou superior com Extension Pack correspondente à versão do VirtualBox.
 2. **Opção 2:** Nesta opção, todo experimento será executado em ambiente local através do download e execução automatizada de todos os componentes utilizando Docker. Para isto, são necessários: Sistema Operacional Linux baseado em Ubuntu versão 20.04 ou mais recente: Ubuntu, Kubuntu, Xubuntu e variantes), processador 64 bits com no mínimo 4 núcleos, 4GB de memória RAM para uso exclusivo no experimento, Docker Engine versão 26 ou superior e alguns pacotes disponíveis no repositório oficial (ver dependências); ou
 3. **Opção 3:** Nesta opção, o ambiente do experimento estará em execução em servidor remoto, em que apenas será necessário o acesso ao desktop virtual deste servidor para sua a execução. Esta opção requer: Sistema Operacional Microsoft Windows 10 ou superior e distribuições Linux baseada em Ubuntu versão 20.04 ou mais recente: Ubuntu, Kubuntu, Xubuntu e variantes, aplicação de remote desktop e cliente de VPN Wireguard.

---

# Dependências

#### O experimento possui três opções disponíveis para execução, tendo cada um deles as seguintes dependências:

 1. **Opção 1:** Cumpridos os requisitos descritos na seção anterior, referentes a **Opção 1**, esta opção não possui dependências.
 2. **Opção 2:** Cumpridos os requisitos descritos na seção anterior, referentes a **Opção 2**, é necessário certificar-se que o Docker Engine versão 26 ou superior esteja instalado conforme descrito na [página oficial da ferramenta](https://docs.docker.com/engine/install/ubuntu/), bem como a seção [postinstall](https://docs.docker.com/engine/install/linux-postinstall/), além dos pacotes __curl__, __rsync__, __wget__ e __git__ instalados.
 3. **Opção 3:** Em Sistema Operacional Linux baseado em Ubuntu versão 20.04 ou mais recente: Ubuntu, Kubuntu, Xubuntu e variantes, é necessário a instalação de aplicação com capacidade de execução RDP (sugere-se xrdp, vinagre ou remmina). Em Sistema Operacional Microsoft Windows 10 ou superior a aplicação RDP é nativa (_mstsc_). Em ambos sistemas operacionais, é requisito a instalação de [cliente de VPN Wireguard](https://www.wireguard.com/install/)

---

# Preocupações com segurança

#### O experimento possui três opções disponíveis para execução, tendo cada um deles as seguintes preocupações com segurança:

 1. **Opção 1:** Por tratar-se de execução de Appliance pronta e virtualizada em ambiente auto contido, não há considerações quanto a preocupações de segurança nesta opção.
 2. **Opção 2:** Durante a execução do conjunto de contêineres envolvidos, dependendo das configurações do dispositivo que estiver hospedando o experimento, as portas **3000**, **8000** e **8080** poderão estar abertas para a rede local, dependendo das configurações de firewall, encaminhamento de portas e perfil de segurança das interfaces de rede. 
 3. **Opção 3:** Por tratar-se de ambiente auto contido e sendo executado em servidor remoto, as implicações de segurança são inerente ao vazamento das credenciais da VPN e do acesso ao servidor. As ações de contenção do ambiente para a proteção do sistema operacional remoto foram tratadas em nível de redução de privilégios, restrição do uso da rede para acesso somente à rede local exclusiva do host e mecanismo de auto destruição e recuperação para o estado anterior, caso necessário.

#### Preocupações adicionais a com segurança

Cabe ressaltar que todas as senhas, chaves de API e outros elementos secretos dos componentes foram gerados para o propósito da demonstração do experimento, de tal forma que sua força de segurança foram propositalmente baixadas para facilitar o experimento. As senhas, chaves de API e chaves RSA do SSH utilizada são descartáveis e servem apenas ao propósito do experimento.

---

# Instalação

#### O experimento possui três opções disponíveis para execução, tendo cada um deles as seguintes etapas de instalação:

### **Opção 1: Appliance de VirtualBox**

1. Baixe o appliance (arquivo .ova) do experimento que está disponível através do [link](https://drive.google.com/file/d/1m7QmK9oirQzBzAiFcbEEvtMOnA4wEZgE/view?usp=sharing).
2. Importe o arquivo __exp-sf-sbseg2025.ova__ baixado no VirtualBox:
   
<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250516_122234.png" alt="Import 01" style="float: left; width: 50%; height: auto;">

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250516_122409.png" alt="Import 02" style="float: left; width: 50%; height: auto;">

3. Clique em _Finalizar_ e aguarde o processo de importação.

4. Execute a VM recém importada.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_141518.png" alt="Import 03" style="float: left; width: 50%; height: auto;">

5. Após a inicialização da VM, abra o terminal (atalho no desktop) e execute:
```bash
iniciar-experimento
```

6. Aguarde a conclusão da preparação do ambiente. Informações do andamento da preparação serão exibidas, bem como informações da básicas da operação do experimento serão exibidas ao término do procedimento.

### **Opção 2: Execução de contêineres localmente**

1. Em um terminal do Linux, executar:
```bash
wget "https://github.com/ljbitzki/experimento-sf-sbseg2025/raw/refs/heads/main/experimento-sf-install.sh" -O "/tmp/experimento-sf-install.sh" ; chmod +x "/tmp/experimento-sf-install.sh" ; /tmp/experimento-sf-install.sh
```
2. Aguarde o término do processo de criação do ambiente.

_(Caso alguma dependência ou requisito anteriormente descrito não tenham sido cumpridos, o script de instalação apresentará em tela as opções de resolução dos elementos faltantes)_

### **Opção 3: Acesso _remote desktop_ ao ambiente em servidor remoto**

1. Em avaliação de viabilidade
2. Em avaliação de viabilidade
3. Em avaliação de viabilidade

---

# Teste mínimo

#### O experimento possui três opções disponíveis para execução, tendo cada um deles os seguintes testes mínimos:

### **Opções 1 e 3: (Appliance de VirtualBox Acesso _remote desktop_ ao ambiente em servidor remoto)**

Estando na máquina virtual recém importada, abrir o terminal e executar:

```bash
docker ps -a
```
Caso o retorno seja uma lista vazia, o Docker Engine estará pronto para a execução do experimento.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_142859.png" alt="Import 04" style="float: left; width: 50%; height: auto;">

### **Opção 2: Execução de contêineres localmente**

Estando logado na máquina virtual recém importada, certificar-se de que há conexão com a internet e o Docker Engine está pronto:
Abra o terminal e execute:

```bash
ping -c 3 github.com
```
<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_143939.png" alt="Import 05" style="float: left; width: 50%; height: auto;">

Caso o retorno seja similar, há conexão com a internet através da máquina virtual.

```bash
docker ps -a
```
Caso o retorno seja uma lista vazia, o Docker Engine estará pronto para a execução do experimento.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_143226.png" alt="Import 06" style="float: left; width: 50%; height: auto;">

* No intuito de evitar quaisquer conflitos entre contêiners existentes no computador (caso o retorno anterior não seja uma lista vazia), sugere-se **parar** todos os contêiners que possam estar rodando localmente, para isso, execute em um terminal:
```bash
while read CID; do docker stop "${CID}"; done < <( docker ps -a | grep -v 'CONTAINER ID' | awk '{print $1}' )
```

---

# Experimentos

#### O experimento possui três opções disponíveis para execução, tendo cada um deles os seguintes etapas para a obtenção das reivindicações:

## Reivindicações: Cenário 1 - Liberação automatizada de porta quando serviço estiver pronto

#### Utilizando as **Opções 1 e 3 (Appliance de VirtualBox e _remote desktop_ no ambiente em servidor remoto**)

Abrir o terminal e executar o alias que verifica o estado do iptables do servidor:

```bash
verificar-firewall-servidor
```

#### Utilizando a **Opção 2 (Execução de contêineres localmente)**

Abrir o terminal e executar o comando para inspecionar o estado do iptables do servidor:

```bash
docker exec -it ubuntu-server iptables -nL
```

Observar a implantação da regra de firewall permitindo o acesso à porta 80 tão logo o contêiner do servidor _nginx_ subiu e ficou pronto para aceitar requisições.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_150925.png" alt="Import 09" style="float: left; width: 50%; height: auto;">

## Reivindicações: Cenário 2 - Mitigação automatizada de ataque DoS

#### Utilizando as **Opções 1 e 3 (Appliance de VirtualBox e _remote desktop_ no ambiente em servidor remoto**)

1. Abrir no navegador **da máquina virtual** o [Netbox](http://localhost:8080/ipam/services/) e o [Grafana](http://localhost:3000/public-dashboards/7d7b1678f7e94829a1816723c251e934?refresh=auto)

#### Utilizando a **Opção 2 (Execução de contêineres localmente)**

1. Abrir no navegador do host que está executando os contêineres o [Netbox](http://localhost:8080/ipam/services/) e o [Grafana](http://localhost:3000/public-dashboards/7d7b1678f7e94829a1816723c251e934?refresh=auto)

Note que em ambos casos o Netbox tem como usuário e senha **admin/admin**

2. No Netbox, verifique que há um serviço HTTP para o _device_ container-nginx. Este serviço foi aplicado como regra de firewall assim que o nginx ficou disponível.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_152105.png" alt="Import 10" style="float: left; width: 50%; height: auto;">

3. No Grafana, observar a baixa contagem de acessos. Os contêineres ubuntu-client e ubuntu-rogue possuem scripts que acessam o contêiner ubuntu-server aleatoriamente de 1 a 9 vezes por segundo, simulando acessos considerados normais.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_152616.png" alt="Import 11" style="float: left; width: 50%; height: auto;">

#### Utilizando as **Opções 1 e 3 (Appliance de VirtualBox e _remote desktop_ no ambiente em servidor remoto**)

4. Abrir um novo terminal e executar o alias para simular um ataque:

```bash
iniciar-ataque
```

#### Utilizando a **Opção 2 (Execução de contêineres localmente)**

4. Abrir um novo terminal e executar o comando para simular um ataque:

```bash
docker exec -it ubuntu-rogue /usr/local/bin/dos.sh
```

5. No Grafana, observar a anomalia no número de acessos. O contêiner ubuntu-rogue dispara uma rajada aleatória entre 100 e 150 acessos por segundo contra o contêiner ubuntu-server, simulando um ataque.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_153002.png" alt="Import 12" style="float: left; width: 50%; height: auto;">

_Note que poucos segundos após o início do ataque, o mesmo foi interrompido. Tão logo o monitoramento percebeu a nomalia no número de acessos, houve a implantação da regra de firewall bloqueando o acesso do IP do atacante._

6. No Netbox, recarregue a página e verifique que há um novo serviço para o _device_ container-nginx. Este serviço foi aplicado como regra de firewall com _source_ do IP do atacante assim que o ataque foi identificado.

<img src="https://github.com/ljbitzki/ljbitzki.github.io/blob/master/Screenshot_20250525_153354.png" alt="Import 13" style="float: left; width: 50%; height: auto;">

#### Utilizando as **Opções 1 e 3 (Appliance de VirtualBox e _remote desktop_ no ambiente em servidor remoto**)

7. Para reiniciar o experimento, pressione Ctrl+C no terminal do comando _iniciar-ataque_ e delete o serviço _DoS_ no Netbox. A remoção do serviço fará o deploy da remoção da regra de bloqueio no firewall do servidor nginx.

#### Utilizando a **Opção 2 (Execução de contêineres localmente)**

7. Para reiniciar o experimento, pressione Ctrl+C no terminal do comando _docker exec -it ubuntu-rogue /usr/local/bin/dos.sh_ e delete o serviço _DoS_ no Netbox. A remoção do serviço fará o deploy da remoção da regra de bloqueio no firewall do servidor nginx.

---

# LICENSE

Este projeto está licenciado sob a Licença GNU - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
