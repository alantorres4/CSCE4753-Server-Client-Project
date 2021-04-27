import sys
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 1234))

dontLeave = True

while dontLeave == True:
	command = input("Input command: (deposit, withdraw, check_balance, exit): ")

	############## DEPOSIT ################
	if command == "deposit":
		client.send(bytes(command, "utf-8")) # make sure this is received from server
		from_server = client.recv(1024)
		if from_server.decode("utf-8") == "OK":
			print("  [+] Command \"deposit\" is received")
			val = input("Input amount: ")
			try:
				Amount = int(val)
			except ValueError:
				print("  [-] Invalid entry. Try an integer.")
				Amount = val

			if isinstance(Amount, int):
				if Amount <= 0:
					print("  [-] A negative or zero amount was entered. Please try again.")
					client.send(bytes(str(Amount), "utf-8")) # Send Amount to server
				else:
					print("  [$] Amount of $" + str(Amount) + ".00 is entered")
					client.send(bytes(str(Amount), "utf-8")) # Send Amount to server
					from_server = client.recv(1024) # If success, output that
					if from_server.decode("utf-8") == "SUCCESS":
						print("  [+] From Server: Operation Succeeded!")
					else:
						print("  [-] From Server: Operation Failed :(")
			else:
				client.send(bytes("44.5", "utf-8"))
		else:
			print("ERROR IN DEPOSIT\n")
			client.send(bytes("ERROR", "utf-8"))

	############### WITHDRAW ###################
	elif command == "withdraw":
		client.send(bytes(command, "utf-8")) # Make sure this is received from server
		from_server = client.recv(1024)
		if from_server.decode("utf-8") == "OK":
			print("  [+] Command \"withdraw\" is received")
			val = input("Input amount: ")
			try:
				Amount = int(val)
			except ValueError:
				print("  [-] Invalid entry. Try an integer.")
				Amount = val

			client.send(bytes(str(Amount), "utf-8")) # Send Amount and error check
			from_server = client.recv(1024)
			answer = from_server.decode("utf-8")

			if answer == "NEGATIVE":
				print("  [-] A negative or zero amount was entered. Please try again.")
			elif answer == "OVERDRAFT":
				print("  [$] Amount of $" + str(Amount) + ".00 is entered.")
				print("  [-] From Server: Operation Failed")
			elif answer == "SUCCESS":
				print("  [$] Amount of $" + str(Amount) + ".00 is entered.")
				print("  [+] From Server: Operation Succeeded!")
			elif answer == "FAIL":
				print("  [$] Amount of $" + str(Amount) + ".00 is entered.")
				print("  [-] From Server: Operation Failed")
		else:
			print("ERROR IN WITHDRAW\n")
			client.send(bytes("ERROR", "utf-8"))


	############ CHECK_BALANCE ##############
	elif command == "check_balance":
		client.send(bytes(command, "utf-8")) # make sure this is received from server
		from_server = client.recv(2048)
		if from_server.decode("utf-8") == "OK":
			print("  [+] Command \"check_balance\" is received")
			client.send(bytes(command, "utf-8")) # send command again to receive balance int
			from_server = client.recv(1024) # receive balance int
			balanceStr = from_server.decode("utf-8")
			print("  [$] From Server: Balance is requested. The balance is $" + balanceStr + ".00")
		else:
			print("ERROR IN CHECK_BALANCE\n")

	########## EXIT ###########
	elif command == "exit":
		print("Command \"exit\" is received\n")

	else:
		print("  [-] Invalid choice.")

	if command == "exit":
		client.close()
		dontLeave = False

