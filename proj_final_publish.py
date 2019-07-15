#!/usr/bin/env python
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver
from message import Message
import pika
import uuid
import os
import time
import random
import csv
import json

class LerDados:

    def __init__(self):

        infile = open('paciente.csv')
        reader = csv.reader(infile)
        mydict = { rows[0] : rows[1]  for rows in reader  }
        self.mydict = mydict

    def getDict(self):
        return self.mydict


#importa os dados do paciente que irá publicar - cria o dict a partir de um csv
def criadicionario():
        with open('paciente.csv', mode='r') as infile:
                reader = csv.reader(infile)
                mydict = {rows[0]:rows[1] for rows in reader}
                print(mydict)
                return mydict
#--------------------------------------------------------------------------


def inputPaciente(resMydict):
        codpac = input ("Entre com o código do paciente (entre 1 e 50):  ")
        print (resMydict[codpac])
        routing_key = resMydict[codpac] #atribui o valor que será o nome da vila
        return codpac, routing_key

#--------------------------------------------------------------------------

def calculaPressao():
        sist = random.choice(range(70,221))
        dias =  random.choice(range(sist - 50, sist - 20))

        dictPressao = {
                "sistolica": sist,
                "diastolica": dias
        }

        pressao = dictPressao
        #pressao = dictPressao
        #print (pressao)
        return pressao

#------ Responsabilidade das funcoes --------------

resMydict = criadicionario() #Cria dicionario
codepac, resRouting_key = inputPaciente(resMydict) #input usuario


#-------------- Loop interações ------------------------------

class FrontEndProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.sendQuote()

    def sendQuote(self):
        print("Messagem  enviada:")
        self.sendLine(self.factory.quote)

    def dataReceived(self, data):
        print( "Received data", data.decode('utf-8') )

        #self.transport.loseConnection()

class FrontEndClientFactory(protocol.ClientFactory):

    def __init__(self, quote):
        self.codes = { 201: ' reply reponse ',
                    200: 'OK'
        }

        self.quote = quote

    def buildProtocol(self, addr):
        return FrontEndProtocol(self)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed {}".format( reason.getErrorMessage() ) )
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Tarefa executada: {} ".format( reason.getErrorMessage() ) )


i = 0

quotes =[]

while (i<=1000):
        resPressao = calculaPressao() # calcula pressao
        message = resPressao

        msg = Message(name=resRouting_key, sensor='sensorpressao', uuid= codepac, tipo= '1', dados=message )
        quotes.append(msg._jsonDump())
        i+=1

for quote in quotes:
    reactor.connectTCP('rabbit01.catalao.ufg.br', 9000, FrontEndClientFactory(quote.encode('utf-8')))


reactor.run()
