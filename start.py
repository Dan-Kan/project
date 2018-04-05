import socket
import pickle
import subprocess
from contextlib import closing
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash
import json


print("REMOTE MANAGER SERVER SETUP")
print("---------------------------")
print()
print("Please provide 3 ports for the server, and two terminal apps: ")
print("IMPORTANT: PORTS MUST BE AVAILABE ON MACHINE")
local_ports = []
while 1:
    port_gen = input("Auto generate free ports? y/n ")
    if port_gen.lower() == "y":
        for i in range(3):
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                s.bind(('', 0))
                local_ports.append(s.getsockname()[1])
        break
    if port_gen.lower() == "n":
        print("Please input ports: ")
        for i in range(3):
            local_ports.append(input())
        break
    else:
        print("Invalid input!")
        continue


print("Local ports to be used: ", local_ports)
print()

with open("config.json", "r+") as f:
    config = json.load(f)
    # update json here
    config["local ports"] = local_ports
    f.seek(0)
    f.truncate()
    json.dump(config, f)


'''
flask_port = 5000
htop_port = 80
terminal_port = 8081

# connection to hostname on the port.
s.connect(("45.77.226.82", 8888))
# s.send(ports)
# Receive no more than 1024 bytes
free_ports = s.recv(4096)
print(pickle.loads(free_ports))
ports = pickle.loads(free_ports)
s.close()

# Pickle turns list to bytes so that it can be sent to server
ports = pickle.dumps([5000, 68, 8081])
'''


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


print("---------------------------")
print("Creating a User: ")
print("This user will be used to log in to the site")
print("---------------------------")
username = input("Username: ")
password = input("Password: ")
print()
print("To change the username and password, change relevant fields in config.json, or run this script again")  # I think
print()

with open("config.json", "r+") as f:
    config = json.load(f)
    config["username"] = username
    f.seek(0)
    f.truncate()
    json.dump(config, f)
    config["password"] = password
    f.seek(0)
    f.truncate()
    json.dump(config, f)


def configure_ssh_tunnel():
    server_ports = []
    print("Please provide 3 ports to be used by the tunneling on the ssh server: ")
    print("IMPORTANT: PORTS MUST BE AVAILABE ON SERVER")

    print("Please input ports: ")
    for i in range(3):
        server_ports.append(input())

    print()
    server_address = input("Please input the server address: ")
    server_addr = input("Please input user and server address (user@server): ")
    json_list = []
    json_list.append(server_address)
    json_list.append(server_addr)
    json_list.append(server_ports)
    with open("config.json", "r+") as f:
        config = json.load(f)
        # update json here
        config["server"] = json_list
        f.seek(0)
        f.truncate()
        json.dump(config, f)

    print("Attempting to create tunnel with ports: ", server_ports)

    command = ["ssh", "-q", "-fN", "-R",
               "{}:localhost:{}".format(server_ports[0], local_ports[0]), server_addr]

    if subprocess.call(command) == 255:
        print("FAILED TO ESTABLISH TUNNEL, EXITING")
        return 255

    command = ["ssh", "-q", "-fN", "-R",
               "{}:localhost:{}".format(server_ports[1], local_ports[1]), server_addr]

    if subprocess.call(command) == 255:
        print("FAILED TO ESTABLISH TUNNEL, EXITING")
        return 255

    command = ["ssh", "-q", "-fN", "-R",
               "{}:localhost:{}".format(server_ports[2], local_ports[2]), server_addr]

    if subprocess.call(command) == 255:
        print("FAILED TO ESTABLISH TUNNEL, EXITING")
        return 255


print("Accessing the server: ")
print("(1) - Manual (Server will open on 0.0.0.0. Requires additional network configuring")
print("(2) - SSH Tunneling (Requires access to external SSH server) (Recommended)")
while 1:
    access_mode = input("1 / 2: ")
    if access_mode == "1":
        json_list = []
        json_list.append("0.0.0.0")
        json_list.append("0.0.0.0")
        json_list.append(local_ports)
        with open("config.json", "r+") as f:
            config = json.load(f)
            # update json here
            config["server"] = json_list
            f.seek(0)
            f.truncate()
            json.dump(config, f)

        print("start server")
        try:
            subprocess.call(["nohup", "python3", "fserver.py", "&", "diswon"])
            print()
            print("Server should now be set up, thanks!")
            break
        except OSError as e:
            print("Execution failed: ", e)
        break
    if access_mode == "2":
        try:
            if configure_ssh_tunnel() == 255:
                print("FAILED TO ESTABLISH TUNNEL, EXITING")
            else:
                subprocess.call(["nohup", "python3", "fserver.py", "&", "diswon"])
                print()
                print("Server should now be set up, thanks!")
                break
        except OSError as e:
            print("Execution failed: ", e)
        break
    else:
        print("Invalid input!")
        continue


# To kill server and all thats related to it:
# ps aux | grep ssh
# kill -9 PID of ssh tunnel (Fress up the ports on remote server as well)
# ps aux | grep python
# kill -9 PID of python3 fserver.py & diswon
# killall gotty
# In order to verify that everything is closed run netstat -tulpn and check for gotty/python/etc...

# https://unix.stackexchange.com/questions/46235/how-does-reverse-ssh-tunneling-work
# https://unix.stackexchange.com/questions/3886/difference-between-nohup-disown-and