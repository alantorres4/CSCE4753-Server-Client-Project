import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((socket.gethostname(), 1234))
serv.listen(5) 

balance = 100

print("The server initialized the bank account")
print("The server is ready to receive requests")

while True:
	conn, addr = serv.accept() # if anyone connects, yay!
	from_client = ''
	while True:
		data = conn.recv(1024) # get the message from client
		print("Server has received the request")

		if not data: break
		from_client = str(data.decode("utf-8")) #change from += data
		print("Server is processing the request")

		################ DEPOSIT ####################
		if from_client == "deposit":
			conn.send(bytes("OK", "utf-8")) # Tell client this was received
			Amount = conn.recv(1024) # Get string Amount from client
			val = Amount.decode("utf-8")

			try:
				AddAmount = int(val)
			except ValueError:
				print("  [-] Not an integer")
				AddAmount = val

			if isinstance(AddAmount, int):
				if AddAmount <= 0:
					print("  [-] Deposit not accepted.\nOperation Failed.")
				else:
					balance += int(AddAmount)
					print("  [+] Deposit is accepted. New balance is $" + str(balance) + ".00\nOperation Succeeded")
					conn.send(bytes("SUCCESS", "utf-8"))
			else:
				print("  [-] NOT AN INTEGER.\nOperation Failed")


		################ WITHDRAW ###################
		elif from_client == "withdraw":
			conn.send(bytes("OK", "utf-8")) # Tell client this was received
			Amount = conn.recv(1024) # Get string Amount from client
			val = Amount.decode("utf-8")

			try:
				WithdrawAmount = int(val)
			except ValueError:
				print("  [-] NOT AN INTEGER")
				WithdrawAmount = val

			if isinstance(WithdrawAmount, int):
				if WithdrawAmount <= 0:
					print("  [-] Amount cannot be withdrawn.\nOperation Failed")
					conn.send(bytes("NEGATIVE", "utf-8"))
				elif WithdrawAmount > balance:
					print("  [-] Overdraft error!\nOperation Failed")
					conn.send(bytes("OVERDRAFT", "utf-8"))
				else:
					balance -= WithdrawAmount;
					print("  [+] Withdraw is accepted. New balance is $" + str(balance) + ".00\nOperation Succeeded")
					conn.send(bytes("SUCCESS", "utf-8"))
			else:
				print("  [-] Amount cannot be withdrawn.\nOperation Failed")
				conn.send(bytes("FAIL", "utf-8"))

		############### CHECK_BALANCE ###################
		elif from_client == "check_balance":
			conn.send(bytes("OK", "utf-8")) # Tell client this was received
			Answer = conn.recv(2048)
			print("  [$] Balance is requested. The balance is $" + str(balance) + ".00")
			conn.send(bytes(str(balance), "utf-8")) # send the balance integer

		############## EXIT ##############
		elif from_client == "exit":
			conn.send(bytes("  [+] SERVER EXITING\n", "utf-8"))

		else:
			conn.send(bytes("  [----] SOMETHING WENT WRONG\n", "utf-8"))


	conn.close()
	print("  [=] Connection with the client is shutdown.")
