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
