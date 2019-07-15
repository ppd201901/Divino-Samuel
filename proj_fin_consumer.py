#!/usr/bin/env python
import pika
import sys
import csv
import json
import time

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
	return routing_key

#--------------------------------------------------------------------------

resMydict = criadicionario()
resRouting_key = inputPaciente(resMydict)
#resRouting_key = "CasoDeTeste1"



credentials = pika.PlainCredentials('admin', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit01.catalao.ufg.br', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='sensorpressao', exchange_type='topic')

result = channel.queue_declare(queue=resRouting_key, durable=True)
queue_name = result.method.queue


binding_keys = resRouting_key
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    print (resRouting_key)
    sys.exit(1)



channel.queue_bind(exchange='sensorpressao', queue=queue_name, routing_key=binding_keys)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
	print (body)
	body = json.loads(body)
	print(" [x] %r:%r" % (method.routing_key, body))
	time.sleep(0.1)



channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)


channel.start_consuming()


connection.close()