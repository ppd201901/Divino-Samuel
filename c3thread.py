import socket
import pickle
import sys
import json


host = '127.0.0.1'  # The server's hostname or IP address
port = 7000        # The port used by the server

#leitura de dados pelo cliente
nome = input('Informe o nome do funcionário: ')
cargo = input('Informe o cargo do funcionário: ')
salario = float (input('Informe o salario do funcionário: '))

print('Cliente 3')

jsondata = '{"nome": "'+nome+'", "cargo": "'+cargo+'", "salario": +salario+}'

dict={}
dict['nome'] = nome
dict ['cargo'] = cargo
dict ['salario'] = salario

jsondata=json.dumps(dict)
print (jsondata)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.send(jsondata.encode())

    data = s.recv(1024)
    drec = json.loads(data.decode())
    print('Recebido- Nome: ',(drec["nome"]))
    print('Recebido- Novo Salário: ',(drec["salario"]))

    print(data.decode())
