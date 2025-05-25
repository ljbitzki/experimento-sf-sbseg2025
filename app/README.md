# README - net2d

## Sobre a Aplicação

O **net2d** é um projeto que visa automatizar a configuração de dispositivos de rede. Atualmente estão suportados apenas dispositivos Mikrotik executando o RouterOS.

## Requisitos

Antes de iniciar a configuração, certifique-se de que possui os seguintes requisitos instalados:

* Processador 64 bits com no mínimo 4 núcleos e flag de virtualzação VT-x ativada na BIOS
* 8GB de RAM exclusivo para o laboratório
* VirtualBox 7.1 ou superior [link](https://www.virtualbox.org/wiki/Downloads)
* VirtualBox Extension Pack 7.1 [link](https://www.virtualbox.org/wiki/Downloads)

### Download do Laboratório

Baixe o laboratório do Net2d que está disponível através de um Appliance do Virtualbox [aqui](https://drive.google.com/file/d/1MJuQxlu-7Nstxtwwlv9CiOo5vvHcApwm/view?usp=sharing).

### Importação do Laboratório

Importe o arquivo _net2d-experimento.ova_ no Virtualbox.

<img src="https://github.com/user-attachments/assets/4400ef0c-6d89-46bf-bdae-8ba328c715f9" alt="Import 01" style="float: left; width: 50%; height: auto;">
<img src="https://github.com/user-attachments/assets/57dcb5e8-d64f-4e1f-9d6e-b827553b43ad" alt="Import 02" style="float: left; width: 50%; height: auto;">


> [!CAUTION]
> É necessário escolher a opção **Include all network adapter MAC address** em *MAC Address Policy*.


<img src="https://github.com/user-attachments/assets/9a439af3-153d-4ee8-9d97-eec5919e4cc2" alt="Import 01" style="float: left; width: 50%; height: auto;">


Clique em *Finish* e aguarde o processo de importação.

## O Ambiente do Laboratório

O laboratório é composto por 7 VMs interconectadas de acordo com a topologia e endereçamento IP a seguir

* 1x Lubuntu 24.04 (net2d-virt)
* 6x RouterOS CHR (rout-lab-0x e host-0x)

<img src="https://github.com/user-attachments/assets/c952e6ce-b82d-41c9-bfb6-b0e1ce169efd" alt="Import 02" style="float: left; width: 50%; height: auto;">
<img src="https://github.com/user-attachments/assets/81944283-9309-44e0-a4e1-3a82970be73c" alt="Import 02" style="float: left; width: 50%; height: auto;">


Estes arquivos estão disponíveis na Área de Trabalho da VM *net2d-virt*. 

### Inicializando o ambiente

Ao selecionar todas as VMs e clicar em *Start*, o Virtualbox emitirá um alerta sobre o consumo de recursos. Clique OK.

<img src="https://github.com/user-attachments/assets/27bf9cf9-2605-4938-8f9d-c67c8cd661d4" alt="Init 01" style="float: left; width: 50%; height: auto;">


> [!NOTE]
> A falta de recursos disponíveis pode ocasionar o erros e as VMs não inicializarem.
> Se isso acontecer em um ambiente linux, tente liberar _cache_ de memória RAM com o comando
> `sudo sh -c 'echo 1 > /proc/sys/vm/drop_caches'`

1. Autentique-se na VM *net2d-virt* com usuário e senha ***net2d/net2d***.
2. Abra um tela do terminal e inicialize o Net2d com o comando
```bash
cd ~/net2d-lab/net2d
docker compose up -d
```

3. Acesse a pasta do Netbox e inicialize-o com o comando
```bash
cd ~/net2d-lab/netbox-docker/
docker compose up -d
```

4. Abra o navegador e acesse o Netbox através do endereço [http://netbox:8080/](http://netbox:8080/).

## O Experimento

O experimento consiste basicamente em comparar os tempos de configuração de dispositivos em um ambiente com a configuração automatizada de ambientes baseados em configuração manual.
Basicamente o processo consiste em:

1. Inicializar o contador de tempo *doc/contrib/ping_all.sh*
2. efetuar as configurações de IP dos roteadores através do Netbox
3. quando todos os hosts tiverem acessíveis, o script será encerrado automaticamente e um arquivo de resultados será salvo em */tmp/results-data-hora.csv*
4. remova as configurações dos roteadores usando o Netbox
5. Executar novamente script ***ping_all.py***
6. configurar manualmente os endereços IPs dos roteadores
7. quando todos os hosts tiverem acessíveis, o script será encerrado automaticamente e um arquivo de resultados será salvo em */tmp/results-data-hora.csv*
8. Ligar a interface de NAT para transmitir os resultados
9. acessar a [página do formulário](https://forms.gle/aawvcpfNzXmvqM5G8) e submeter os arquivos de resultado.

Para iniciar o experimento siga os passos a seguir.

### 1. Inicializando o contador de tempo

Dentro da VM net2d-virt, abra uma janela de terminal, acesse a pasta do net2d e execute o script monitor de tempos *ping_all*
```bash
cd net2d-lab/net2d
python3 doc/contrib/ping_all.py
```

### 2. Configure os Roteadores via Netbox (Configuração Automatizada)

1. Abra o navegador dentro da VM net2d-virt e acesse o Netbox em [http://netbox:8080/](http://netbox:8080/).
2. Acesse o menu ***IPAM > IP Address***
3. Conforme a Tabela de Endereçamento, pesquise, acesse a página de detalhes do IP **172.18.52.1/23** e clique em *Editar*

<img src="https://github.com/user-attachments/assets/272e2895-68c9-41f1-be61-800abe8fa88c" alt="Import 02" style="float: left; width: 50%; height: auto;">


4. Associe o IP à interface **ether2** do **rout-lab-01** e salve a mudança

<img src="https://github.com/user-attachments/assets/495acc9e-02e5-4266-adc3-9cee2aae539a" alt="Import 02" style="float: left; width: 50%; height: auto;">


6. **Repita a operação até configurar as interfaces ***ether2***, ***ether3*** e ***ether4*** de todos os roteadores**.
   
7. Se as configurações forem realizadas corretamente e todos os IPs dos hosts-01, host-02 e host-03 estiverem acessíveis (ping!) a configuração é considerada finalizada e o script contador de tempo será finalizado automaticamente.

### 3. Configure os Roteadores via CLI (Configuração Manual)

#### Preparação

1. Remova as configurações de IP realizadas na etapa anterior, mantendo apenas o IP de Gerência da **ether1**.
<img src="https://github.com/user-attachments/assets/a0c05aa6-a555-4481-8c6d-d44d61a2d3f8" alt="Import 02" style="float: left; width: 50%; height: auto;">

3. Certifique-se que as configurações foram removidas dos roteadores conectando à CLI dos roteadores via SSH com credenciais ***admin/admin***. Para o rout-lab-01, por exemplo, execute:
```
ssh admin@192.168.1.101
/ip/address/print
```
<img src="https://github.com/user-attachments/assets/e9401b47-8d98-4baf-b815-a5d3fcbdce65" alt="Import 02" style="float: left; width: 50%; height: auto; margin-bottom: 10px">

#### Configuração Manual

1. Inicialize o contador de tempo. Abra uma janela de terminal, acesse a pasta do net2d e execute o script monitor de tempos *ping_all*
```bash
cd net2d-lab/net2d
python3 doc/contrib/ping_all.py
```

2. Em outra janela de terminal, acesse cada um dos roteadores e configure os endereços IPs através da CLI. Para o rout-lab-01 interface ether2, por exemplo, o comando seria:
```
/ip/address/add address=172.18.52.1/23 interface=ether2
```

3. **Repita a operação até configurar as interfaces ***ether2***, ***ether3*** e ***ether4*** de todos os roteadores**.

4. Se as configurações forem realizadas corretamente e todos os IPs dos hosts-01, host-02 e host-03 estiverem acessíveis (ping!) a configuração é considerada finalizada e o script contador de tempo será finalizado automaticamente.


## Enviando os resultados

Quando o script **ping_all.py** executa com sucesso e pinga todos os hosts, ele salva os resultados em um arquivo .csv em /tmp.
Para enviar estes resultados, é necessário primeiro ativar a interface NAT para a VM *net2d-virt* para ter acesso à internet.

1. Para ativar a interface de NAT, clique em Network Settings na janela da VM
<img src="https://github.com/user-attachments/assets/d6973cc8-d507-447d-aab7-1cb9e3fd7a3b" alt="Import 02" style="float: left; width: 50%; height: auto;">


3. Configure o Adapter 1 para usar NAT e conecte o cabo.
<img src="https://github.com/user-attachments/assets/cd6f7e3f-a20f-480c-ace8-a9d49b009b76" alt="Import 02" style="float: left; width: 50%; height: auto;">


5. Abra o navegador e acesse a [página do formulário](https://forms.gle/aawvcpfNzXmvqM5G8) de envio dos resultados.
6. Siga as instruções da página.
