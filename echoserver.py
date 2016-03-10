from socket import *
from select import *

sock = socket(AF_INET,SOCK_STREAM)
sock.bind(('',10000))
sock.listen(100)

input = [sock]
output = []
data = {}


while(True):
    r,w,e = select(input,output,[])
    for s in r:
        if s == sock:
            cli,addr = s.accept()
            print addr
            input.append(cli)
        else:
            content = s.recv(100)
            if not content:
                input.remove(s)
                s.close()
            else:
                data[s] = content
                input.remove(s)
                output.append(s)
    for s in w:
        content = data.pop(s)
        s.send(content)
        output.remove(s)
        input.append(s)
