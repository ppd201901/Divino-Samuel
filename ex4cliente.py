#!/usr/bin/env python3

import socket
import pickle
import sys
import json


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#leitura de dados pelo cliente
nome = input('Informe o nome: ')
altura = float (input('Informe a altura: '))
sexo =  input('Informe o sexo F - feminino / M - masculino: ')

#jsondata = '{"nome": "'+nome+'", "cargo": "'+cargo+'", "salario": '+salario+'}'
dict={}
dict['nome'] = nome
dict ['altura'] = altura
dict ['sexo'] = sexo

jsondata=json.dumps(dict)
print (jsondata)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(str.encode(jsondata))
    #s.send(jsondata.encode("utf-8"))
    
    data = s.recv(1024)
    drec = json.loads(data.decode("utf-8"))
    print('Recebido- Nome: ',(drec["nome"]))
    print('Recebido- Peso Ideal: ',(drec["pesoideal"]))