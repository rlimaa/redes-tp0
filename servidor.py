from struct import *
import socket
HOST = ''
PORT = 51515
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket "anzol" (que aceita novas conexoes)
orig = (HOST, PORT)
s.bind(orig)
s.listen(1)
global_counter = 0 #inicia o contador em 0
while True:
	new_s, cliente = s.accept()
	new_s.settimeout(1) #configura o timeout para 1s
	try: #tratamento de exceção
		op = new_s.recv(8) #recebe a operacao a ser realizada
		aux = global_counter #salva o valor do contador, caso ocorra um erro na transmissao
		if op == '+': #se a operacao desejada for soma
			if global_counter < 999: #se o contador e menor q 999
				global_counter += 1 #incrementa o contador
			else: #caso o contador seja 999
				global_counter = 0 #contador volta para 0
		elif op == '-': #se a operacao desejada for subtracao
			if global_counter > 0: #caso o contador seja maior que 0
				global_counter -= 1 #decrementa o contador
			else: #caso o contador seja 0
				global_counter = 999 #vai para 999
		new_s.send(pack('!i', global_counter)) #envia o proximo valor do contador para o cliente
		confirm_gc = new_s.recv(24)#recebe a confrimacao do cliente
		new_s.close() #encerra a conexao
		if int(confirm_gc) == global_counter: #se a confirmacao do cliente esta correta
			print global_counter #imprime o contador
		else #senao
			global_counter = aux #contador nao e atualizado
	except socket.timeout: #se ocorrer a excecao timeout
		print 'T' #imprime T
		new_s.close(); #fecha a conexao
