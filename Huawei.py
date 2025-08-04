from netmiko import ConnectHandler


devices=[
    {"device_type":"huawei",
    "host":"192.168.42.",
    "port":"",
    "username":"",
    "password":""},

    {"device_type":"huawei",
    "host":"192.168.42.167",
    "port":"",
    "username":"",
    "password":""},

    {"device_type": "huawei",
     "host": "192.168.42.",
     "port": "",
     "username": "",
     "password": ""},

    {"device_type": "huawei",
     "host": "192.168.42.169",
     "port": "11233",
     "username": "",
     "password": ""}
]



ip_config={
    "192.168.42.159":{"int ether 1/0/0":{"ip":"68.1.1.1", "mask":"30"},"int ether 1/0/1":{"ip":"38.1.1.1","mask":"30"},
                      },
"192.168.42.167":{"int ether 1/0/0":{"ip":"68.1.1.2", "mask":"30"},"int ether 1/0/1":{"ip":"78.1.1.1","mask":"30"},
                  },
"192.168.42.168":{"int ether 1/0/0":{"ip":"38.1.1.2", "mask":"30"},"int ether 1/0/1":{"ip":"48.1.1.1","mask":"30"},
                  },
"192.168.42.169":{"int ether 1/0/0":{"ip":"78.1.1.2", "mask":"30"},"int ether 1/0/1":{"ip":"48.1.1.2","mask":"30"},
                  },
}

mpls_config={"192.168.42.159":{"lsr-id":"1.1.1.1"},
"192.168.42.167":{"lsr-id":"2.2.2.2"},
"192.168.42.168":{"lsr-id":"3.3.3.3"},
"192.168.42.169":{"lsr-id":"4.4.4.4"}
             }

isis_config={
    "192.168.42.159":{"process":"isis 1", "id":"network-entity 59.0000.0192.0168.0420.0159.00"},
"192.168.42.167":{"process":"isis 1", "id":"network-entity 67.0000.0192.0168.0420.0167.00"},
"192.168.42.168":{"process":"isis 1", "id":"network-entity 68.0000.0192.0168.0420.0168.00"},
"192.168.42.169":{"process":"isis 1", "id":"network-entity 69.0000.0192.0168.0420.0169.00"},
}

ospf_config={"192.168.42.159":{"process":"37727","area":"area 0","net":"68.1.1.0","wildcard":"0.0.0.3","network":"38.1.1.0","mask":"0.0.0.3"},
             "192.168.42.167":{"process":"37727","area":"area 0","net":"68.1.1.0","wildcard":"0.0.0.3", "network":"78.1.1.0","mask":"0.0.0.3"},
             "192.168.42.168":{"process":"37727","area":"area 0","net":"38.1.1.0","wildcard":"0.0.0.3", "network":"48.1.1.0","mask":"0.0.0.3"},
             "192.168.42.169":{"process":"37727","area":"area 0","net":"78.1.1.0","wildcard":"0.0.0.3", "network":"48.1.1.0","mask":"0.0.0.3"},
             }



def configure_ip_addresses(connection,ip):
    for interface, ip_config in ip.items():
        commands=[f"{interface}", f"ip add {ip_config['ip']} {ip_config['mask']}","mpls",'mpls ldp',"isis enable 1","ospf enable 1 area 0","commit"]
        output=connection.send_config_set(commands)
        print(output)

def configure_mpls(connection,mpls):
    commands=[f"mpls lsr-id {mpls['lsr-id']}","mpls","mpls ldp","commit"]
    output = connection.send_config_set(commands)
    print(output)


def configure_isis(connection,isis):
    commands=[f"{isis['process']}",f"{isis['id']}","commit","quit"]
    output = connection.send_config_set(commands)
    print(output)

def configure_ospf(connection,ospf):
    commands=[f"ospf {ospf['process']}",f"{ospf['area']}",f"network {ospf['net']} {ospf['wildcard']}",f"network {ospf['network']} {ospf['mask']}","commit"]
    output=connection.send_config_set(commands)
    print(output)



def configure_rt(connection):

    output = connection.send_command("disp ospf peer br")
    print(output)


def configure_router(device,ip_config,mpls_config,isis_config,configure_rt,ospf_config):
    connection=ConnectHandler(**device)
    
    print(f"connected to {device['host']}")
    if device['host']in mpls_config:
     mpls=mpls_config[device['host']]
     #configure_mpls(connection,mpls)



    if device['host']in isis_config:
     isis=isis_config[device['host']]
     #configure_isis(connection,isis)

    if device['host']in ospf_config:
     ospf=ospf_config[device['host']]
     configure_ospf(connection, ospf)

    if device['host'] in ip_config:
     ip = ip_config[device['host']]
     #configure_ip_addresses(connection,ip)

     #configure_mpls(connection,mpls)
    #configure_isis(connection,isis)
    #configure_ip_addresses(connection,ip)
    #configure_ospf(connection,ospf)
    configure_rt(connection)
    #connection.save_config()



for device in devices:
    try:
        configure_router(device,ip_config,mpls_config,isis_config,configure_rt, ospf_config)
    except Exception as e:
        print("failed to connect to: ", e)
