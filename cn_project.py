from socket import AF_INET, SOCK_STREAM, socket
from base64 import *
import ssl
import smtplib
import socks
import base64
# import socket 

#'proxy_port' should be an integer
#'PROXY_TYPE_SOCKS4' can be replaced to HTTP or PROXY_TYPE_SOCKS5
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, 'localhost', 587)
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 9050)
socks.wrapmodule(smtplib)

#socket.getaddrinfo('localhost',8080)

smtp = smtplib.SMTP()
#add in prompt
userEmail = input("Enter Your Email Address: ")
userPassword = input("Enter Your Password: ")
userDestinationEmail = input("Enter Email Destination: ")
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")




msg = '{}.\r\n I love computer networks!'.format(userBody)
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'
mailPort = 587
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, mailPort))
#Fill in end
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
# Send hello command and print server response.
heloCommand = 'HELO Ashvin\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')
 
#account authentication
strtlscmd = "STARTTLS\r\n".encode()
clientSocket.send(strtlscmd)
revc2 = clientSocket.recv(1024)


sslClientSocket = ssl.wrap_socket(clientSocket)


# emailA = base64.b64encode(userEmail.encode)
# emailP = base64.b64encode(userPassword.encode)
emailA = base64.b64encode(bytes(userEmail,"UTF-8"))
emailP = base64.b64encode(bytes(userPassword,"UTF-8"))

authorizationCMD = "AUTH LOGIN\r\n"


sslClientSocket.send(authorizationCMD.encode())
recv2 = sslClientSocket.recv(1024)
print(recv2)


sslClientSocket.send(emailA + "\r\n".encode())
recv3 = sslClientSocket.recv(1024)
print(recv3)


sslClientSocket.send(emailP + "\r\n".encode())
recv4 = sslClientSocket.recv(1024)
print(recv4)




# Send MAIL FROM command and print server response.
# Fill in start
mailFrom = "Mail from: <{}>\r\n".format(userDestinationEmail)
sslClientSocket.send(mailFrom.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5)
# Fill in end
# Send RCPT TO command and print server response.
# Fill in start
rcptto = "RCPT TO: <{}>\r\n".format(userDestinationEmail)
sslClientSocket.send(rcptto.encode())
recv6 = sslClientSocket.recv(1024)
print(recv6)
# Fill in end
# Send DATA command and print server response.
# Fill in start
data = 'DATA\r\n'
sslClientSocket.send(data.encode())
recv7 = sslClientSocket.recv(1024)
print(recv7)
# Fill in end
# Send message data.
# Fill in start
sslClientSocket.send("Subject: {}\n\n{}".format(userSubject, msg).encode())
# Fill in end
# Message ends with a single period.
# Fill in start
sslClientSocket.send(endmsg.encode())
recv8 = sslClientSocket.recv(1024)
print(recv8)
# Fill in end
# Send QUIT command and get server response.
# Fill in start
quitCMD = 'QUIT\r\n'
sslClientSocket.send(quitCMD.encode())
recv9 = sslClientSocket.recv(1024)
print(recv9)


sslClientSocket.close()
print('Success')
# Fill in end