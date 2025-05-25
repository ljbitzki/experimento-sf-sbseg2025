import ipaddress
import pynetbox
import logging
import os
import ansible_runner
from api.models import Sot
from celery import shared_task
from celery.utils.log import get_task_logger
from netmiko import ConnectHandler, BaseConnection
from ipaddress import ip_address, ip_interface, ip_network
from jinja2 import Environment, FileSystemLoader

logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    return x + y


@shared_task
def sw_deploy_task(device_id):

    print('Iniciando deploy')
    logger.info('Iniciando deploy Device Netbox: ' + str(device_id))

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    nb_device = netbox.dcim.devices.get(id=device_id)
    
    # Monta o Journal Entry para associar ao Device
    comments = 'Iniciando deploy via Net2D'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.device'
    journal_entry['assigned_object_id'] = device_id
    journal_entry['kind'] = 'info'
    journal_entry['comments'] = comments

    # Cria o Journal associado ao Device
    nb_journal = netbox.extras.journal_entries.create(journal_entry)
    print(nb_journal)

    # Tarefa de Deploy
    logger.info('Iniciando Deploy do Device Netbox: ' + str(device_id))

    ##########################################
    ######## Configuração de Básicas #########
    ##########################################
    logger.info('Iniciando Configurações básicas..')
    task_result = config_basic(device_id)

    ##########################################
    ###### Configuração de Interfaces ########
    ##########################################
    logger.info('Iniciando configuração de Interfaces')
    task_result = config_interfaces(device_id)
    # logger.info(task_result)

    # Monta o Journal Entry para associar ao Device
    comments = 'Finalizado o deploy.'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.device'
    journal_entry['assigned_object_id'] = nb_device.id
    journal_entry['kind'] = 'info'
    journal_entry['comments'] = comments
    # Cria o Journal associado ao Device
    nb_journal = netbox.extras.journal_entries.create(journal_entry)
    print(nb_journal)

@shared_task
def interface_deploy_task(interface_id):

    print('Iniciando deploy')
    logger.info('Iniciando deploy Interface Netbox: ' + str(interface_id))

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    nb_interface = netbox.dcim.interfaces.get(id=interface_id)
    
    # Monta o Journal Entry para associar ao Device
    comments = 'Iniciando deploy via Net2D'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.interface'
    journal_entry['assigned_object_id'] = interface_id
    journal_entry['kind'] = 'info'
    journal_entry['comments'] = comments

    # Cria o Journal associado ao Device
    nb_journal = netbox.extras.journal_entries.create(journal_entry)
    print(nb_journal)

    # ##########################################
    # ###### Configuração da Interface ########
    # ##########################################
    logger.info('Iniciando configuração da Interface')
    task_result = config_one_interface(interface_id)
    logger.info(task_result)

    # Monta o Journal Entry para associar ao Device
    comments = 'Finalizado o deploy.'
    journal_entry = {}
    journal_entry['assigned_object_type'] = 'dcim.interface'
    journal_entry['assigned_object_id'] = nb_interface.id
    journal_entry['kind'] = 'info'
    journal_entry['comments'] = comments
    # Cria o Journal associado ao Device
    nb_journal = netbox.extras.journal_entries.create(journal_entry)
    print(nb_journal)


def config_basic(device_id):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    # Busca dispositivo na Sot
    nb_device = netbox.dcim.devices.get(id=device_id)

    # Carrega os templates do Jinja2
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("mikrotik_device_basic_config.yml.jinja")

    # Renderiza um Playbook
    filename = f"/app/api/playbooks/mikrotik_{nb_device.name}.yml"
    content = template.render(
        hostname = ip_interface(nb_device.primary_ip4).ip.compressed,
        device_name=nb_device.name
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
    logger.info("Criado o playbook: ")
    logger.info(content)

    # Executando o Playbook gerado
    logger.info("Executando playbook: ")
    runner = ansible_runner.run(playbook=filename)
    logger.info("{}: {}".format(runner.status, runner.rc))
    logger.info("Final status:")
    logger.info(runner.stats)
    



def config_interfaces(device_id):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    # Busca Dispositivo e Interfaces na Sot
    nb_device = netbox.dcim.devices.get(id=device_id)
    nb_interfaces = netbox.dcim.interfaces.filter(device_id=nb_device.id)

    # Cria um playbook para configurar os IPs em cada interface 
    ip_addresses = []
    for iface in nb_interfaces:
        if iface["mode"] == None:
            if iface["type"] != "virtual":
                nb_if_ips = netbox.ipam.ip_addresses.filter(assigned_object_id=iface.id)
                for ip in nb_if_ips:
                    address = {}
                    address["address"] = ip.address
                    address["interface"] = iface.name
                    ip_addresses.append(address)

    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("tasks.yml.jinja")

    filename = f"/app/api/playbooks/set_device_{nb_device.name.lower()}.yml"
    content = template.render(
        hostname = ip_interface(nb_device.primary_ip4).ip.compressed,
        ip_addresses = ip_addresses
    )

    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
    logger.info("Criado o playbook: ")
    logger.info(content)

    # Executando o Playbook gerado
    logger.info("Executando playbook: ")
    runner = ansible_runner.run(playbook=filename)
    logger.info("{}: {}".format(runner.status, runner.rc))
    logger.info("Final status:")
    logger.info(runner.stats)

    return 1


def config_one_interface(interface_id):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    # Busca Interface na Sot
    nb_interface = netbox.dcim.interfaces.get(id=interface_id)
    nb_if_ips = netbox.ipam.ip_addresses.filter(assigned_object_id=nb_interface.id)
    nb_device = netbox.dcim.devices.get(nb_interface.device["id"])

    ip_addresses = []
    for ip in nb_if_ips:
        address = {}
        address["address"] = ip.address
        ip_addresses.append(address)


    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("config_one_interface.yml.jinja")

    filename = f"/app/api/playbooks/set_one_interface_{nb_device.name.lower()}_{nb_interface.name.lower()}.yml"
    content = template.render(
        hostname = ip_interface(nb_device.primary_ip4).ip.compressed,
        interface = nb_interface.name,
        ipv4_addresses = ip_addresses,
    )

    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
    logger.info("Criado o playbook: ")
    logger.info(content)

    # Executando o Playbook gerado
    logger.info("Executando playbook: ")
    runner = ansible_runner.run(playbook=filename)
    logger.info("{}: {}".format(runner.status, runner.rc))
    logger.info("Final status:")
    logger.info(runner.stats)

    return 1


def get_vlans(device_id):
    vlans = []

    sot = Sot.objects.get(name="netbox-lab")

    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token

    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )
    # Busca o dispositivo
    nb_device = netbox.dcim.devices.get(id=device_id)
    # Busca as interfaces do dispositivo
    nb_interfaces = netbox.dcim.interfaces.filter(device_id=nb_device.id)
    logger.info("Contando as Vlans do dispositivo: " + nb_device.name)
    for interface in nb_interfaces:
        if interface['mode'] != None:    
            # Se a Interface for Tagged ou Access
            # recolhe todas as Vlans
            if interface['mode']['value'] == 'access':
                vlans.append(interface['untagged_vlan'])
            if interface['mode']['value'] == 'tagged':
                if interface['untagged_vlan'] != None:
                    vlans.append(interface['untagged_vlan'])                
                for vlan in interface['tagged_vlans']:
                    vlans.append(vlan)
    logger.info("Vlans encontradas: " + str(vlans))
    vlan_ids = list({v['id']:v for v in vlans}.values())
    logger.info("Vlans Ids encontrados: " + str(vlan_ids))
    return vlan_ids

@shared_task
def svc_deploy_task(service_id,event,data):
    # Tentar acesso por chave ssh
    # ssh_key_path = "/app/api/env/ssh_key"
    print('Iniciando deploy')
    logger.info('Iniciando deploy para o Service: ' + str(service_id))

    # Recebe o tipo de evento e todos os dados da requisição anterior, necessário para consultar o prechange
    service_event = event
    request_data = data
    
    # ###########################################
    # ###### Chamada do config_one_service ######
    # ###########################################
    logger.info('Iniciando configuração do Service')
    if service_event == 'created':
        task_result = add_one_rule_service(service_id)
    if service_event == 'deleted':
        task_result = del_one_rule_service(service_id,request_data)
    if service_event == 'updated':
        task_result = del_one_rule_service(service_id,request_data)
        task_result = add_one_rule_service(service_id)
    #task_result = config_one_service(service_id,service_event,request_data)
    logger.info(task_result)

#def config_one_service(service_id,ssh_key_path,event,request_data):
def add_one_rule_service(service_id):

    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )

    # Busca Service na Sot
    nb_service = netbox.ipam.services.get(id=service_id)
    service_id = nb_service.id
    service_name = nb_service.name
    service_ports = nb_service.ports[0]
    service_proto = nb_service.protocol.value
    service_ip_address = nb_service.ipaddresses[0]
    service_tag = str(nb_service.tags[0].id)
    service_source = nb_service.custom_fields['source']
    service_description = nb_service.description
    service_comments = nb_service.comments

    # Cria inventory para o host
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("base-inventory.yml.jinja")
    ipint = ipaddress.IPv4Interface(service_ip_address)
    inventory_filename = f"/app/api/inventories/{service_id}_{service_ports}_{service_proto}.yml"
    inventory_content = template.render(
        ip_address = str(ipint.ip)
    )
    # Escreve arquivo inventory para o host no workdir /app/api/inventories/
    with open(inventory_filename, mode="w", encoding="utf-8") as message:
        message.write(inventory_content)
        print(f"... wrote {inventory_filename}")
    logger.info("Criado o inventory: ")
    logger.info(inventory_content)

    # Cria playbook para a ação de incluir regra
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("iptables-add-accept.yml.jinja")
    if service_tag == '1':
        template = environment.get_template("iptables-add-accept.yml.jinja")
    if service_tag == '2':
        template = environment.get_template("iptables-add-drop.yml.jinja")
    playbook_filename = f"/app/api/playbooks/set_one_service_{service_id}.yml"
    playbook_content = template.render(
        name = service_name,
        ports = service_ports,
        protocol = service_proto,
        ip_address = service_ip_address,
        source = service_source,
        description = service_description,
        comments = service_comments,
    )

    with open(playbook_filename, mode="w", encoding="utf-8") as message:
        message.write(playbook_content)
        print(f"... wrote {playbook_filename}")
    logger.info("Criado o playbook: ")
    logger.info(playbook_content)

    # Executa o Playbook gerado com sudo, necessário para manipular o iptables
    logger.info("Executando playbook: ")
    runner = ansible_runner.run(
        inventory=inventory_filename,
        playbook=playbook_filename,
        extravars={
            'ansible_become': True,
            'ansible_become_user': "root",
            'ansible_user': "net2d",
        },
        )
    logger.info("{}: {}".format(runner.status, runner.rc))
    logger.info("Final status:")
    logger.info(runner.stats)

    return 1

def del_one_rule_service(service_id,request_data):
    # Extrai informações do service nos dados recebidos do snapshot e cria playbook de remoção
    old_name = request_data['snapshots']['prechange']['name']
    old_ports = request_data['snapshots']['prechange']['ports'][0]
    old_tags = request_data['snapshots']['prechange']['tags'][0]
    old_proto = request_data['snapshots']['prechange']['protocol']
    old_ipaddress = request_data['data']['ipaddresses'][0]['address']
    old_source = request_data['snapshots']['prechange']['custom_fields']['source']
    old_description = request_data['snapshots']['prechange']['description']
    old_comments = request_data['snapshots']['prechange']['comments']

    # Cria inventory para o host
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("base-inventory.yml.jinja")
    ip = ip_interface(old_ipaddress)
    inventory_filename = f"/app/api/inventories/{service_id}_{old_ports}_{old_proto}.yml"
    inventory_content = template.render(
        ip_address = ip.ip
    )

    with open(inventory_filename, mode="w", encoding="utf-8") as message:
        message.write(inventory_content)
        print(f"... wrote {inventory_filename}")
    logger.info("Criado o inventory: ")
    logger.info(inventory_content)

    # Criando playbook de remoção de regra existente
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("iptables-del.yml.jinja")
    playbook_filename = f"/app/api/playbooks/del_one_service_{service_id}.yml"
    playbook_content = template.render(
        name = old_name,
        ports = old_ports,
        protocol = old_proto,
        source = old_source,
        description = old_description,
        comments = old_comments,
        tag = old_tags,
    )

    with open(playbook_filename, mode="w", encoding="utf-8") as message:
        message.write(playbook_content)
        print(f"... wrote {playbook_filename}")
    logger.info("Criado o playbook: ")
    logger.info(playbook_content)

    # Executa o playbook gerado
    logger.info("Executando playbook: ")
    runner = ansible_runner.run(
        inventory=inventory_filename,
        playbook=playbook_filename,
        extravars={
            'ansible_become': True,
            'ansible_become_user': "root",
            'ansible_user': "net2d",
        },
        )
    logger.info("{}: {}".format(runner.status, runner.rc))
    logger.info("Final status:")
    logger.info(runner.stats)

def device_services(device_id):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )
    # Filtra e retorna os ids dos serviços associados ao device
    nb_services = netbox.ipam.services.filter(device_id=device_id)
    services = []
    for s in nb_services:
        services.append(s.id)
    return services

def device_persistent_services(device_id,svc):
    # Inicializa cliente API da fonte de verdade
    sot = Sot.objects.get(name="netbox-lab")
    netbox_url = "http://" + sot.hostname + ":" + str(sot.port) + "/"
    netbox_token = sot.token
    netbox = pynetbox.api(
        netbox_url,
        token=netbox_token
    )
    nb_service = netbox.ipam.services.get(id=svc)
    service_ports = nb_service.ports[0]
    service_proto = nb_service.protocol.value
    service_ip_address = nb_service.ipaddresses[0]
    service_source = nb_service.custom_fields['source']
    service_description = nb_service.description
    service_comments = nb_service.comments
    # Cria arquivo de regras persistentes
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("iptables-persistent.yml.jinja")
    playbook_filename = f"/app/api/playbooks/services_{device_id}.yml"
    playbook_content = template.render(
        ports = service_ports,
        protocol = service_proto,
        source = service_source,
        source_file = playbook_filename,
        description = service_description,
        comments = service_comments,
        new_line = ''
    )

    with open(playbook_filename, mode="a", encoding="utf-8") as message:
        message.write(playbook_content)
        print(f"... wrote {playbook_filename}")

    # Cria inventory para o host
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("base-inventory.yml.jinja")
    ip = ip_interface(service_ip_address)
    inventory_filename = f"/app/api/inventories/{device_id}.yml"
    inventory_content = template.render(
        ip_address = ip.ip
    )

    with open(inventory_filename, mode="w", encoding="utf-8") as message:
        message.write(inventory_content)
        print(f"... wrote {inventory_filename}")
    logger.info("Criado o inventory: ")
    logger.info(inventory_content)

@shared_task
def apply_device_persistent_services(device_id):
    inventory_filename = f"/app/api/inventories/{device_id}.yml"
    # Cria arquivo de regras persistentes
    environment = Environment(loader=FileSystemLoader("/app/api/templates/"))
    template = environment.get_template("apply-iptables-persistent.yml.jinja")
    playbook_filename = f"/app/api/playbooks/services_apply_{device_id}.yml"
    playbook_content = template.render(
        device_id = device_id,
    )

    with open(playbook_filename, mode="a", encoding="utf-8") as message:
        message.write(playbook_content)
        print(f"... wrote {playbook_filename}")

    # Executa o playbook gerado
    logger.info("Executando playbook: ")
    runner = ansible_runner.run(
        inventory=inventory_filename,
        playbook=playbook_filename,
        extravars={
            'ansible_become': True,
            'ansible_become_user': "root",
            'ansible_user': "net2d",
        },
        )
    logger.info("{}: {}".format(runner.status, runner.rc))
    logger.info("Final status:")
    logger.info(runner.stats)
