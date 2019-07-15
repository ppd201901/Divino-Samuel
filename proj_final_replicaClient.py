import logging
import socket

class ReplicaClient:

    '''
        Classe para conectar os clientes com os servidores de replicas
        e transmitir as replicas para os mesmos.
    '''

    def __init__(self, server):
        self.host, self.port = server

    def connect(self, msg):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            try:
                s.connect((self.host, self.port))
                s.sendall(msg.encode('utf-8'))
                data = s.recv(1024)

                data = data.decode('utf-8')
                print(data)
            except socket.error as m:
                print("Socket binding error {}".format(m))
            finally:
                s.close()
