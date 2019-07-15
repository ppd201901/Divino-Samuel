#!/usr/bin/env python
import pika

from multiprocessing import Pool

def funcConnect(x):
	credentials = pika.PlainCredentials('admin', 'password')
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host = '200.137.238.18', port = 5672, credentials = credentials))
	channel = connection.channel()
	channel.queue_declare(queue='hello')
	connection.close()



with Pool(10) as p:
	a = p.map(funcConnect, list(range(2)))
	p.close()
	p.join()


print(" [x] Sent 'Hello World!'")