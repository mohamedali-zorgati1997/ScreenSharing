#V 1.0
import PIL.ImageGrab as image
import socket
import threading
from io import BytesIO
import queue
Q = queue.Queue()
PORT = 80

def get_ip(): # makes a fake connection to get the IP address of the server
    try:
        u = socket.socket(type=socket.SOCK_DGRAM)
        u.connect(("1.1.1.1",1))
        return u.getsockname()[0]
    except:
        return "unknown ip address" # probably 127.0.0.1
def thread(): # this function takes care of every client 
    while True:
        try:
            c,a = Q.get() # wait and get the client socket
            print("incoming connection : {}:{}".format(*a))
            print("recv: ",c.recv(1028).split(b'\n', 1)[0].strip())
            c.send(b"HTTP/1.0 200 OK\r\nServer: Python/3\r\nContent-Type: image/png\r\n\r\n")
            img = BytesIO()
            image.grab().save(img, "PNG") # convert the image to PNG and save it to a stream
            c.send(img.getvalue())
            c.close()
        except Exception as e:
            print("Error: ",e)

server =  socket.socket()
server.bind(('',PORT))
server.listen(5)
print("Starting Server!")
for _ in range(4): # handle 4 connections at the same time
    t = threading.Thread(target=thread)
    t.setDaemon(True)
    t.start()
print("Listening on IP: {}".format(get_ip()))
while True:
    try:
        Q.put(server.accept()) # keep listening for incoming connection and add it to the queue
    except KeyboardInterrupt:
        server.close()
        print("Have a nice day")
        exit(0)

