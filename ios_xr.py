from netmiko import ConnectHandler
import json
import getpass

with open("cred.json")as file:
    cred=json.load(file)
    username=cred['username']
    password=cred['password']



devices=[]
target_ips=["192.168.42.11","192.168.42.12"]

for ip in target_ips:
    device = {"device_type": "cisco_ios",
              "host": ip,
              "port": "22",
              "username": username,
              "password": password
              }
    devices.append(device)




with open("ip_config.json")as f:
    ip_config=json.load(f)

with open("mpls_config.json")as f:
    mpls_config=json.load(f)

with open("ospf_config.json")as f:
    ospf_config=json.load(f)

with open("vpws_config.json")as f:
    vpws_config=json.load(f)

with open("vpls_config.json")as f:
    vpls_config=json.load(f)

with open("isis_config.json")as f:
    isis_config=json.load(f)

def configure_ip_address(connection,ip):
    for interface,ip_config in ip.items():
        commands=[f"{interface}",f"ipv4 address {ip_config['ip']}","no shut", "commit"]
        output=connection.send_config_set(commands)
        print(output)


def configure_mpls(connection,mpls):
    commands=["mpls ldp",f"interface {mpls['int']}", f"interface {mpls['intb']}","commit"]
    output=connection.send_config_set(commands)
    print(output)


def configure_ospf(connection,ospf):
    commands=["router ospf 1","address-family ipv4",f"{ospf['area']}",f"{ospf['a']}",
             f"{ospf['b']}",f"{ospf['c']}","commit"]
    output=connection.send_config_set(commands)
    print(output)

def configure_isis(connection,isis):
    commands=["router isis 1","address-family ipv4","exit",f"{isis['inta']}","address-family ipv4",
              "exit",f"{isis['intb']}","address-family ipv4","exit",
              f"{isis['intc']}","address-family ipv4","exit","commit"]
    output=connection.send_config_set(commands)
    print(output)





def configure_l2vpn_vpws(connection,l2vpn):
    commands=["l2vpn","xconnect group pe1_to_pe2","p2p pe1_to_pe2",f"{l2vpn['inta']}",
              f"neighbor {l2vpn['peer']} pw-id {l2vpn['pw-id']}",
              "commit"]
    output=connection.send_config_set(commands)
    print(output)


def configure_l2vpn_vpls(connection,vpls):
    commands=["l2vpn","bridge group l2vpn","bridge-domain l2vpn",f"{vpls['int']}","exit",
    f"vfi {vpls['name']}",f"neighbor {vpls['peer']} pw-id {vpls['id']}","commit"]
    output=connection.send_config_set(commands)
    print(output)



def configure_router(device):
    connection=ConnectHandler(**device)
    connection.enable()
    print(f"connecting to {device['host']}")
    ip=ip_config[device['host']]
    #mpls=mpls_config[device['host']]
    #ospf=ospf_config[device['host']]
    #isis=isis_config[device['host']]
    #l2vpn=vpws_config[device['host']]
    #vpls=vpls_config[device['host']]

    configure_ip_address(connection,ip)
    #configure_mpls(connection,mpls)
    #configure_ospf(connection,ospf)
    #configure_l2vpn_vpws(connection,l2vpn)
    #configure_l2vpn_vpls(connection,vpls)
    #configure_isis(connection,isis)

for device in devices:
    try:
        configure_router(device)
    except Exception as e:
        print("device configuration failed: ", e)





