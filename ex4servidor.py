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
            print (load["altura"])
            print (load["sexo"])

            condicao = load["sexo"]
            altura = load['altura']
            formula = 0

            if condicao == "f":
                formula = (62.1 * altura) - 44.7
            elif condicao == "m":
                formula = (72.7 * altura) - 58
           

            load["pesoideal"] = formula
            

            resend=json.dumps(load)
            print (resend)

            if not load:
                break
            conn.sendall(str.encode(resend))