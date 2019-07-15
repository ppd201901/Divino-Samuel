#!/usr/bin/env python3

import socket
import pickle
import sys
import json


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#leitura de dados pelo cliente
nome = input('Informe o nome do aluno: ')
nota1 = float (input('Informe o primeira nota: '))
nota2 = float (input('Informe o segunda nota: '))
#nota3 = float (input('Informe o terceira nota: '))
resultado = 'a definir'

#jsondata = '{"nome": "'+nome+'", "sexo": "'+sexo+'", "idade": '+idade+'}'
dict={}
dict['nome'] = nome
dict ['nota1'] = nota1
dict ['nota2'] = nota2
#dict ['nota3'] = nota3
#dict ['resultado'] = resultado

jsondata=json.dumps(dict)
print (jsondata)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(str.encode(jsondata))
    #s.send(jsondata.encode("utf-8"))
    while True:
    	data = s.recv(1024)
    	drec = json.loads(data.decode("utf-8"))
    	print('Recebido- Aluno: ',(drec["nome"]))
    	print('Recebido- Média: ',(drec["media"]))
    	print('Recebido- Resultado: ',(drec["resultado"]))

    	if (drec["resultado"]) == 'N3':
    		nota3 = float (input('Informe o terceira nota: '))
    		dict ['nota3'] = nota3
    		jsondata=json.dumps(dict)
    		print (jsondata)
    		s.sendall(str.encode(jsondata))
    		data = s.recv(1024)
    		drec = json.loads(data.decode("utf-8"))
    		print('Recebido- Aluno: ',(drec["nome"]))
    		print('Recebido- Média: ',(drec["media"]))
    		print('Recebido- Resultado: ',(drec["resultado"]))
    	
    	elif not data:
    		break