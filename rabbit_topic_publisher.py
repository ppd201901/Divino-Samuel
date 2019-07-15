#!/usr/bin/env python
import pika
import sys
import time
from random import choice 

credentials = pika.PlainCredentials('admin', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq.catalao.ufg.br', credentials=credentials))

channel = connection.channel()
channel.exchange_declare(exchange='topic_class', exchange_type='topic')


topics = ['EDPA', 'PPD', 'SEM']
alunos = ['Samuel' , 'Divino', 'Carlos', 'Paulo', 'Junior', 'Felipe']


while(True):
    routing_key = choice(topics)
    message = choice(alunos)
    print('Send -> {0} -- {1}'.format(routing_key, message))
    channel.basic_publish(
        exchange='topic_class', routing_key=routing_key, body=message)

    time.sleep(0.5)
    


connection.close()




#routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
#message = ' '.join(sys.argv[2:]) or 'Hello World!'

#print(" [x] Sent %r:%r" % (routing_key, message))
#connection.close()
