#! /usr/bin/env python3
import paramiko,xmltodict 
from flask import Flask, jsonify
app = Flask(__name__)
def serverAccess (host, username, pswd, port, fileName) :
  client = paramiko.client.SSHClient ()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect (hostname=host, username=username, password=pswd, port=port) 
  stdin, stdout , stderr=client. exec_command( 'nvidia-smi -q -x')
  output = stdout.readlines()
  if output != "":
    file = open(fileName, 'w')
    file.write("".join (output))
    file.close()

@app.route('/servers/<int:i>', methods=['GET']) 
def getServerData(i: int) :
  try:
    host,user,pswd, port, file = tableServers [str(i)]
    serverAccess (host, user, pswd, port, file) 
    with open(file) as fd:
      server = xmltodict.parse(fd.read())
    return jsonify(server)
  except Exception as e:
    print(e)
    return jsonify({'error':'Server does not exist.'}), 404

class Server():
  def __init__(self,port,pathComplement,pswd):
     self.end,self.userName,self.path,self.port = '172.26.5.55','valeria','/root/config/sensores/data/'+pathComplement,port
     self.pswd = '4GM3M' if pswd == '' else pswd

  def get(self): return [self.end,self.userName,self.pswd,self.port,self.path]

server1,server2,server3,server4 = Server(102,'server1/Server1_Data.xml',''),Server(112,'server2/Server2_Data.xml',''),Server(122,'server3/Server3_Data.xml',''),Server(132,'server4/Server4_Data.xml','velma')
tableServers = {'1':server1.get(),'2':server2.get(),'3':server3.get(),'4':server4.get()}
app.run(host="0.0.0.0")
