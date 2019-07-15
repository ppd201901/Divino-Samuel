from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol
from threading import Thread
from hashlib import md5
from uuid import uuid4
import json
import socket

class ReplicaManagerProtocol(LineReceiver):

    '''
          response codes:
          200 =>  ok
          201 =>  Requisição já esta registrada
          300 =>  GR não é o primario
          404 =>  resquest mal formadas json com erros
          500 =>  publish encaminha msg
    '''

    def __init__(self, factory):
        self.factory = factory
        self.hashcode = None
        self.statusCode = 200
        self.response =  None
        self.state = None

    def jsonDump(self, dic):
        return json.dumps(dic)

    def lineReceived(self, line):
        if self.state == 'NEW':
            self.handle_NEW(line)

    def connectionMade(self):
        self.state = 'NEW'

    def connectionLost(self, reason):
        self.sendLine("200".encode())

    def handle_NEW(self, line):
        #self.sendLine("200".encode('utf-8'))

        if not self.factory.Primary:
            self.state = 'CLOSE'
            self.statusCode = 300
            self.handle_CLOSE()

        self.state = "REGISTER"
        self.handle_REGISTER(line)

    def handle_REGISTER(self, line):
        try:
            self.hashcode = md5(line).hexdigest()
            payload = json.loads(line.decode("utf-8"))


            if self.hashcode in self.factory.request.keys():
                self.state = 'RESPONSE'
                self.statusCode = 201
                self.handle_RESPONSE()
            else:
                self.factory.request[self.hashcode] = payload
                self.state = 'EXECUTION'
                self.handle_EXECUTION(payload)

        except ValueError:
            print("Error")
            self.statusCode = 404
            self.state = 'RESPONSE'
            self.handleRESPONSE()

    def handle_EXECUTION(self, req):
        from rabbitmq import RabbitMQ

        login = self.factory.rabbit['login']
        password = self.factory.rabbit['password']
        ip = self.factory.rabbit['ip']

        routingkey =  req['topic']
        exchange   = req['exchange']
        tipo = req['tipo']

        rabbit = RabbitMQ(login=login, password=password,
                          server=ip, exchange=exchange, routingkey=routingkey   )

        if tipo == '1':   #'publish'
            msg = req['payload']
            msg = json.dumps(msg)
            rabbit.publish(msg)
            self.statusCode = '500'
            self.factory.response[self.hashcode] = self.statusCode

        self.state = 'REPLICATION'
        self.handle_REPLICATION(req)


    def handle_REPLICATION(self, req):
        print("REPLICATION")

        from replicaClient import ReplicaClient
        import threading

        msg = self.jsonDump(req)

        PORT = 10000
        grs = self.factory.grServers
        servers =  [ (i, PORT)  for i in grs ]
        replicas = []

        for i in servers:
            replicas.append( ReplicaClient(i) )

        threads = [ threading.Thread(target=client.connect, args=(msg,)) for client in replicas]
        for thread in threads:
            thread.start()
            thread.join()

        self.state = 'RESPSONSE'
        self.handle_RESPONSE()

    def handle_RESPONSE(self):
        print("REPONSE")
        self.sendLine( self.statusCode.encode("utf-8") )


    def handle_CLOSE(self):
        return

class ReplicaManagerServer(Factory):

    '''
        Class Factory for connection mode
    '''

    def __init__(self):
        self.uidServer = str(uuid4())
        self.request = {}
        self.response = {}
        #self.grServers = ['18.221.109.240', '13.58.158.80']
        self.grServers = ['127.0.0.1' ]
        #self.grServers = ['rabbit02.catalao.ufg.br', 'rabbit03.catalao.ufg.br']
        self.Primary = True

        self.rabbit = {
            'ip' : '13.59.149.70',
            'login': 'admin',
            'password': 'password'
        }


    def buildProtocol(self, addr):
        #print(addr)
        return ReplicaManagerProtocol(self)

reactor.listenTCP(9000, ReplicaManagerServer())
reactor.run()
