from netmiko import ConnectHandler
import getpass
username = input("Username: ")
password = getpass.getpass("Password: ")    

devices=[
    {"device_type":"huawei",
    "host":f"192.168.42.{i}",
    "port":"11233",
    "username":username,
    "password":password
    }

for i in range(170,174)
]



ip_config={
    "192.168.42.170":{"int ether 1/0/0":{"ip":"68.1.1.1", "mask":"30"},"int ether 1/0/1":{"ip":"38.1.1.1","mask":"30"}, "int loopback0":{"ip":"1.1.1.1","mask":"32"}
                      },


"192.168.42.171":{"int ether 1/0/0":{"ip":"48.1.1.1", "mask":"30"},"int ether 1/0/1":{"ip":"38.1.1.2","mask":"30"},
                 "int loopback0": {"ip":"3.3.3.3","mask":"32"}
                  },

"192.168.42.172":{"int ether 1/0/0":{"ip":"78.1.1.1", "mask":"30"},"int ether 1/0/1":{"ip":"48.1.1.2","mask":"30"},
                 "int loopback0":{"ip":"4.4.4.4","mask":"32"}
                  },

"192.168.42.173":{"int ether 1/0/0":{"ip":"68.1.1.2", "mask":"30"},"int ether 1/0/1":{"ip":"78.1.1.2","mask":"30"},
                "int loopback0":  {"ip": "2.2.2.2", "mask": "32"}
                  },
}



mpls_config={"192.168.42.170":{"lsr-id":"1.1.1.1"},
"192.168.42.171":{"lsr-id":"3.3.3.3"},
"192.168.42.172":{"lsr-id":"4.4.4.4"},
"192.168.42.173":{"lsr-id":"2.2.2.2"}
             }

isis_config={
    "192.168.42.170":{"process":"isis 1", "id":"network-entity 59.0000.0192.0168.0420.0159.00"},
"192.168.42.171":{"process":"isis 1", "id":"network-entity 67.0000.0192.0168.0420.0167.00"},
"192.168.42.172":{"process":"isis 1", "id":"network-entity 68.0000.0192.0168.0420.0168.00"},
"192.168.42.173":{"process":"isis 1", "id":"network-entity 69.0000.0192.0168.0420.0169.00"},
}

ospf_config={"192.168.42.170":{"process":"37727","area":"area 0","net":"68.1.1.0","wildcard":"0.0.0.3","network":"38.1.1.0","mask":"0.0.0.3"},
             "192.168.42.171":{"process":"37727","area":"area 0","net":"48.1.1.0","wildcard":"0.0.0.3", "network":"38.1.1.0","mask":"0.0.0.3"},
             "192.168.42.172":{"process":"37727","area":"area 0","net":"78.1.1.0","wildcard":"0.0.0.3", "network":"48.1.1.0","mask":"0.0.0.3"},
             "192.168.42.173":{"process":"37727","area":"area 0","net":"68.1.1.0","wildcard":"0.0.0.3", "network":"78.1.1.0","mask":"0.0.0.3"},
             }

## vsi-config
vsi_config= {
   "192.168.42.170": {"peer":"2.2.2.2"},
             "192.168.42.173":{"peer":"1.1.1.1"}
             }

##mpls ldp l2vpn configuration
mpls_ldp_remote_peer={"192.168.42.170": {"name":"R2", "remote_ip":"2.2.2.2"},
             "192.168.42.173":{"name":"R1", "remote_ip":"1.1.1.1"}
             }

##l2vpn binding to interfaces
l2vpn_binding={"192.168.42.170": {"interface":"int ether 1/0/3"},
             "192.168.42.173": {"interface":"int ether 1/0/3"}
             }



def configure_ip_addresses(connection,ip):
    for interface, ip_config in ip.items():
        commands=[f"{interface}", f"ip add {ip_config['ip']} {ip_config['mask']}"," ospf enable 37727 area 0","commit","undo isis enable 1","commit"]
        output=connection.send_config_set(commands)
        print(output)

def configure_mpls(connection,mpls):
    commands=[f"mpls lsr-id {mpls['lsr-id']}","mpls","mpls ldp","commit"]
    output = connection.send_config_set(commands)
    print(output)


def configure_isis(connection,isis):
    commands=[f"undo {isis['process']}","y"]
    output = connection.send_config_set(commands)
    print(output)

def configure_ospf(connection,ospf):
    commands=[f"ospf {ospf['process']}",f"{ospf['area']}",f"network {ospf['net']} {ospf['wildcard']}",f"network {ospf['network']} {ospf['mask']}","commit"]
    output=connection.send_config_set(commands)
    print(output)

def configure_vsi(connection, vsi):
   commands= ["mpls l2vpn","commit","quit","vsi test", "encapsulation ethernet","mtu 1500","pwsignal ldp",
              "vsi-id 1234",
              f"peer {vsi['peer']}","commit" ]
   output = connection.send_config_set(commands)
   print(output)


def configure_mpls_ldp_remote_peer(connection, mpls_ldp):
    commands = [f"mpls ldp remote-peer {mpls_ldp['name']}", 
                f"remote-ip {mpls_ldp['remote_ip']}",
                "commit"
                  ]
    output = connection.send_config_set(commands)
    print(output)

def configure_l2vpn_binding(connection, l2vpn):
    commands = [f"{l2vpn['interface']}", "l2 binding vsi test",
            
                "commit"      ]
    output = connection.send_config_set(commands)
    print(output)



def configure_rt(connection):
    commands=[ "disp ospf peer br","disp vsi"]
    output=connection.send_config_set(commands)
    print(output)



def configure_router(device):
    connection=ConnectHandler(**device)
    
    print(f"connected to {device['host']}")
    if device['host']in mpls_config:
     mpls=mpls_config[device['host']]




    if device['host']in isis_config:
     isis=isis_config[device['host']]


    if device['host']in ospf_config:
     ospf=ospf_config[device['host']]


    if device['host'] in ip_config:
     ip = ip_config[device['host']]
     
    if device['host'] in vsi_config:
        vsi = vsi_config[device['host']]
        
    
    if device['host'] in mpls_ldp_remote_peer:
        mpls_ldp = mpls_ldp_remote_peer[device['host']]

    if device['host'] in l2vpn_binding:
        l2vpn = l2vpn_binding[device['host']]
        


    #configure_mpls(connection,mpls)
    #configure_isis(connection,isis)
    #configure_ip_addresses(connection,ip)
    #configure_ospf(connection,ospf)
    configure_vsi(connection, vsi)
    #configure_mpls_ldp_remote_peer(connection, mpls_ldp)
    #configure_l2vpn_binding(connection, l2vpn)
    configure_rt(connection)
    connection.save_config()



for device in devices:
    try:
        configure_router(device)
    except Exception as e:
        print("failed to connect to: ", e)
