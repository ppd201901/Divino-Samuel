import socket
import pickle
import sys
import json

from _thread import *

host = ''
port = 7000

sckthr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#print('Conexão estabelecida em: %s:%d ' % (host, port))

#try:
sckthr.bind((host, port))
#except socket.error:
#	print('conexão de um cliente finalizada')
#	sys.exit()


sckthr.listen(10)

print("Escutando")

def testethread(conn):

	while True:
		data = conn.recv(1024)
		#print(conn)

		load = json.loads(data.decode('UTF-8'))
		#print (type(load))
		#print('Recebido:',(load))
		print (load["nome"])
		print (load["cargo"])
		print (load["salario"])
		condicao = load["cargo"]
		salario = load["salario"]
		if condicao == "operador":
			percentual = 0.20
		elif condicao == "programador":
			percentual = 0.18
		else:
			percentual = 0

		aumento = percentual * salario
		novo_salario = salario + aumento

		load["salario"] = novo_salario

		resend=json.dumps(load)
		print (resend)

		if not load:
			break
		conn.sendall(str.encode(resend))
		
	
	conn.close()

while 1:
		conn, addr = sckthr.accept()
		start_new_thread(testethread, (conn,))

#sckthr.close()


