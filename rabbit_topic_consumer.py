#!/usr/bin/env python
import pika
import sys

class ClassMates:

    def __init__(self):
        credentials = pika.PlainCredentials('admin', 'password')
        #Conecta na maquina rabbitMQ 
        self.connection = pika.BlockingConnection( pika.ConnectionParameters(host='rabbitmq.catalao.ufg.br',
                                                                             credentials=credentials))
        self.channel = self.connection.channel()

        # Cria um exchange do tipo topico 
        self.channel.exchange_declare(exchange='topic_class', exchange_type='topic')
        #declara uma nova fila que recebera um nome aleatorio 
        res = self.channel.queue_declare('', exclusive=True)
        self.queue_name = res.method.queue

    def callback(self, ch, method, properties, body):
        print('{0} -> {1} '.format(method.routing_key, body))

    def subscribe(self, topic_key):
         self.channel.queue_bind(exchange='topic_class', queue=self.queue_name, routing_key=topic_key)
         
         self.channel.basic_consume(queue=self.queue_name,
                                    on_message_callback=self.callback, auto_ack=True)
         print("[-] Waiting for Classmates Connections. --->")
         self.channel.start_consuming()


if __name__ == '__main__':

    binding_key = sys.argv[1]
    if not binding_key:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    classmates = ClassMates()
    classmates.subscribe(binding_key)
    
