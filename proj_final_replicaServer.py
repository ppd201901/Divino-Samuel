import threading
import socket
import time
import logging
import socketserver
import sys
import types
import json
from random import choice

class MyTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


class ReplicaServer(socketserver.BaseRequestHandler):


    def connectReplica(self, msg):
        from rabbitmq import RabbitMQ
        login = 'admin'
        password = 'password'
        ip = '18.221.109.240'

        routingkey =  msg['topic']
        exchange   = msg['exchange']
        tipo = msg['tipo']
        rabbit = RabbitMQ(login=login, password=password,
                          server=ip, exchange=exchange, routingkey=routingkey   )

        if tipo == '1':   #'publish'
            req = msg['payload']
            print(req)
            req = json.dumps(req)
            rabbit.publish(req)

    def handle(self):

        try:
            data = self.request.recv(1024).strip()
            msg = json.loads(data)
            self.connectReplica(msg)
            self.request.sendall(bytes('ok', 'UTF-8'))
        except Exception as e:
            print("Exceptiion wile receiving message {}".format(e))

def server(host, port):

    ser = socketserver.TCPServer((host, port), ReplicaServer)
    ser.serve_forever()

if __name__ == '__main__':


    #host , port = sys.argv[1], int(sys.argv[2])

    server('127.0.0.1', 10000)
