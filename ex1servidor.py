#!/usr/bin/env python3

import socket
import pickle
import sys
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print ("escutando na porta: %s:%d" % (HOST,PORT))
    conn, addr = s.accept()
    with conn:
        print('Connected em: ',(addr))
        while True:
            data = conn.recv(1024)

            load = json.loads(data.decode("utf-8"))
            
            print (type(load))
            print('Recebido:',(load))
            print (load["nome"])
            print (load["cargo"])
            print (load["salario"])

            condicao = load["cargo"]
            salario = load["salario"]

            if condicao == "operador":
                percentual = 0.20
            elif condicao == "programador":
                percentual = 0.18
            else:
                percentual = 0

            aumento = percentual * salario
            novo_salario = salario + aumento

            load["salario"] = novo_salario
            

            resend=json.dumps(load)
            print (resend)

            if not load:
                break
            conn.sendall(str.encode(resend))