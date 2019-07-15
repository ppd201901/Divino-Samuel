#!/usr/bin/env python3

import socket
import pickle
import sys
import json


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#leitura de dados pelo cliente
nome = input('Informe o nome da pessoa: ')
sexo = input('Informe o sexo: ')
idade = int (input('Informe a idade: '))
maioridade = 'identificar'

#jsondata = '{"nome": "'+nome+'", "sexo": "'+sexo+'", "idade": '+idade+'}'
dict={}
dict['nome'] = nome
dict ['sexo'] = sexo
dict ['idade'] = idade
dict ['maioridade'] = maioridade

jsondata=json.dumps(dict)
print (jsondata)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(str.encode(jsondata))
    #s.send(jsondata.encode("utf-8"))
    
    data = s.recv(1024)
    drec = json.loads(data.decode("utf-8"))
    print('Recebido- Nome: ',(drec["nome"]))
    print('Recebido- Maior Idade: ',(drec["maioridade"]))