#!/usr/bin/env python3

import socket #biblioteca socket
import pickle #biclioteca para o dump e load
import sys
import json #biblioteca para passar um json

HOST = '127.0.0.1'  # ip localhost
PORT = 65432        # porta

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #socket.AF_INET - endreço ipv4, socket.SOCK_STREAM - relativo a porta tcp
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
            print (load["sexo"])
            print (load["idade"])

            condicao = load["sexo"]
            idade = load["idade"]
            maioridade = load["maioridade"]

            if condicao == "feminino":
                if idade > 21:
                    maioridade = 'sim'
                else: maioridade = 'não'
            elif condicao == "masculino":
                if idade > 18:
                    maioridade = 'sim'
                else: maioridade = 'não'
            else:
                maioridade = 0

            load["maioridade"] = maioridade
            

            resend=json.dumps(load)
            print (resend)

            if not load:
                break
            conn.sendall(str.encode(resend))