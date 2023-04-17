import base64
import ssl
from socket import AF_INET, SOCK_STREAM, socket
from tkinter import *
import time 



# create a function that will send the email
def sendEmail():
    userEmail = email.get()
    userPassword = password.get()
    userDestinationEmail = destination.get()
    userSubject = subject.get()
    # take the body of the email and add a new line to the end of the message
    userBody = body.get("1.0", END) + "\r\n"

    msg = '{}.\r\n'.format(userBody)
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) and call it mailserver
    if 'gmail.com' in userEmail:
        mailserver = 'smtp.gmail.com'
        mailPort = 587
    elif 'yahoo.com' in userEmail:
        mailserver = 'smtp.mail.yahoo.com'
        mailPort = 587

    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((mailserver, mailPort))
    except Exception as e:
        print(f"Error connecting to {mailserver} on port {mailPort}: {e}")
        return

    recv = clientSocket.recv(1024).decode()
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send hello command and print server response.
    heloCommand = 'HELO Ashvin\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()

    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # account authentication
    strtlscmd = "STARTTLS\r\n".encode()
    clientSocket.send(strtlscmd)
    revc2 = clientSocket.recv(1024)

    time.sleep(3)

    sslClientSocket = ssl.wrap_socket(clientSocket)

    if 'gmail.com' in userEmail:
        # authentication for gmail
        print("gmail")
        emailA = base64.b64encode(bytes(userEmail, "UTF-8"))
        emailP = base64.b64encode(bytes(userPassword, "UTF-8"))
        authorizationCMD = "AUTH LOGIN\r\n"
        sslClientSocket.send(authorizationCMD.encode())
        recv2 = sslClientSocket.recv(1024)
        sslClientSocket.send(emailA + "\r\n".encode())
        recv3 = sslClientSocket.recv(1024)
        sslClientSocket.send(emailP + "\r\n".encode())
        recv4 = sslClientSocket.recv(1024)
    elif 'yahoo.com' in userEmail:
        # authentication for yahoo
        print("yahoo")
        emailFull = userEmail
        authID = base64.b64encode(bytes(emailFull, "UTF-8"))
        authPassword = base64.b64encode(bytes(userPassword, "UTF-8"))
        authorizationCMD = "AUTH PLAIN\r\n"
        sslClientSocket.send(authorizationCMD.encode())
        recv2 = sslClientSocket.recv(1024)
        authString = '\0{}\0{}'.format(emailFull, userPassword)
        authString = base64.b64encode(bytes(authString, "UTF-8"))
        sslClientSocket.send(authString + "\r\n".encode())
        recv3 = sslClientSocket.recv(1024)
    # Send MAIL FROM command and print server response.
    mailFromCommand = "MAIL FROM:<{}>\r\n".format(userEmail)
    sslClientSocket.send(mailFromCommand.encode())
    recv5 = sslClientSocket.recv(1024)

    # Send RCPT TO command and print server response.
    rcptToCommand = "RCPT TO:<{}>\r\n".format(userDestinationEmail)
    sslClientSocket.send(rcptToCommand.encode())
    recv6 = sslClientSocket.recv(1024)

    # Send DATA command and print server response.
    dataCommand = "DATA\r\n"
    sslClientSocket.send(dataCommand.encode())
    recv7 = sslClientSocket.recv(1024)

    # Send message data.
    sslClientSocket.send("Subject: {}\n\n{}".format(userSubject, msg).encode())

    # Message ends with a single period.
    sslClientSocket.send(endmsg.encode())
    recv8 = sslClientSocket.recv(1024)

    # Send QUIT command and get server response.
    quitCommand = "QUIT\r\n"
    sslClientSocket.send(quitCommand.encode())
    recv9 = sslClientSocket.recv(1024)

    # Close connection with clientSocket and sslClientSocket.
    clientSocket.close()
    sslClientSocket.close()
    print('Success')

    # close the GUI
    root.destroy()


# make the GUI more user friendly and better looking
root = Tk()
# set the title of the GUI with center alignment
root.title("Email Client")
root.geometry("500x350")
root.resizable(0, 0)

# position the GUI in the center of the screen
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
root.geometry("+{}+{}".format(positionRight, positionDown))


# create a frame
app = Frame(root)
app.grid()

# create a label with entry boxes and position them in the grid
Label(app, text="Email Client", font=("Helvetica", 30)).grid(
    row=0, column=1, sticky=W, columnspan=2)


Label(app, text="Enter Your Email Address: ").grid(row=1, column=0, sticky=W)
email = Entry(app)
email.config(width=30)
email.grid(row=1, column=1, sticky=W)

Label(app, text="Enter Your Password: ").grid(row=2, column=0, sticky=W)
password = Entry(app)
password.config(width=30, show="*")
password.grid(row=2, column=1, sticky=W)

Label(app, text="Enter Email Destination: ").grid(row=3, column=0, sticky=W)
destination = Entry(app)
destination.config(width=30)
destination.grid(row=3, column=1, sticky=W)

Label(app, text="Enter Subject: ").grid(row=4, column=0, sticky=W)
subject = Entry(app)
subject.config(width=30)
subject.grid(row=4, column=1, sticky=W)

Label(app, text="Enter Message: ").grid(row=5, column=0, sticky=W)
# create a text box for the body of the email and increase the size of the text box so you can see the whole message
body = Text(app, width=39, height=10)
body.grid(row=5, column=1, sticky=W)


# create a button where when clicked it will take the information from the entry boxes and send the email
button = Button(app, text="Send Email", command=sendEmail)
button.grid(row=6, column=0, sticky=W)


# start the GUI
root.mainloop()
