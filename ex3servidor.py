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
        data = conn.recv(1024)

        load = json.loads(data.decode())
        
        #print (type(load))
        print('Recebido:',(load))
        #print (load["nome"])
        #print (load["nota1"])
        #print (load["nota2"])

        nome = load["nome"]
        nota1 = load["nota1"]
        nota2 = load["nota2"]

        media = (nota1 + nota2) / 2
        resultado = 'a definir'

        if media >= 7:
            resultado = 'aprovado'
        elif media <= 3:
            resultado = 'reprovado'

        if media > 3 and media < 7:
            resultado = 'N3'       
            load["media"] = media
            load['resultado'] = resultado      
            resend=json.dumps(load)
            print (resend)
            conn.send(str.encode(resend))

            data = conn.recv(1024)
            load = json.loads(data.decode())
            #print (type(load))
            print('Recebido:',(load))
            nota3 = load["nota3"]
            media = (media + nota3) / 2
            if media >= 5:
                resultado = 'aprovado'
            else: resultado = 'reprovado'

        load["media"] = media
        load['resultado'] = resultado            
        resend=json.dumps(load)
        print (resend)
        conn.send(str.encode(resend))
        s.close()
