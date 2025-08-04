from netmiko import ConnectHandler
import os

backup="backups"
os.makedirs(backup,exist_ok=True)

devices=[{"device_type":"",
         "host":f"192.168.42.{i}",
         "port":"22",
         "username":"",
          "password":"",
         "secret":""}
         for i in range(,)
         ] 





for device in devices:
    try:
        net_connect=ConnectHandler(**device)
        print(f"connecting to {device['host']}")
        net_connect.enable()
        output=net_connect.send_command("disp curr")
        print(output)
        filename=(f"{device['host']}_config.txt")
        filepath=os.path.join(backup,filename)
        with open(filepath,"w")as file:
            file.write(output)
    except Exception as e:
        print("failed to configure device :",e)














