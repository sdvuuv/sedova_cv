import numpy as np
import matplotlib.pyplot as plt
import socket

host = "84.237.21.36"
port = 5152

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data

def checkstar(img, y, x):
    if(img[y][x] <= img[y][x+1]):
        return False
    if(img[y][x] <= img[y+1][x]):
        return False
    if(img[y][x] <= img[y][x-1]):
        return False
    if(img[y][x] <= img[y-1][x]):
        return False
    return True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host,port))
    for i in range(10):
        sock.send(b"get")
        bts = recvall(sock, 40002)
            
        im1 = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0],
                                                                bts[1])
        poslist = []
        for y in range(1, im1.shape[0]-1):
            for x in range(1, im1.shape[1]-1):
                if checkstar(im1, y, x):
                    poslist.append(y)
                    poslist.append(x)
                
                    
        try:            
            dist = round(np.sqrt((poslist[2]-poslist[0])**2 + (poslist[3] - poslist[1])**2), 1)  
        except IndexError:
            print(poslist)
            
            break
        sock.send(f"{dist}".encode())
        print(f"{sock.recv(20)} {i+1}-е изображение")   
    
    sock.send(b"beat")
    beat = sock.recv(20)
    print(f"{beat} - финальный вердикт")
    plt.imshow(im1) 
    plt.show()
    
