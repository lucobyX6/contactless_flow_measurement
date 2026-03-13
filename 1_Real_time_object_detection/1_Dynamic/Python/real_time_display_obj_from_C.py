import serial
from queue import Queue
from threading import Thread
import numpy as np
from time import sleep

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def read_values(serialPort : serial, com_fifo : Queue):
    reading = False
    tmp_values = []
    
    while(1):
        serialString = str(serialPort.readline().decode("Ascii"))

        if("start" in serialString):
            reading = True
            tmp_values = []
        
        if("end" in serialString):
            reading = False
            if(tmp_values[0][0] !=0):
                com_fifo.put(tmp_values)

        if(reading == True and "start" not in serialString):
            tmp_values.append(serialString[:-1].split(","))

    sleep(0.05)

def animate(i):     
    
    values = com_fifo.get()
    i=0
    j=0

    matrice_distances = np.zeros((8,8))
    matrice_objects = np.zeros((8,8))
    for index in range(len(values[0])):
        if(index%2 == 0):    
            matrice_distances[i][j] = values[0][index]
        else: 
            matrice_objects[i][j] = values[0][index]
            j+=1     
            if(j == 8):
                i +=1
                j =0

    ax1.clear()  
    color = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]

    tmp = []
    for i in range(len(matrice_objects)):
        for j in range(len(matrice_objects)):
            index = int(matrice_objects[i][j])
            if(index >= len(color)):
                index = index%len(color)
            tmp.append(color[index])
    
    x = []
    y = []
    z = []

    for i in range(len(matrice_distances)):
        for j in range(len(matrice_distances[0])):
            x.append(i)
            y.append(j)
            z.append(matrice_distances[i][j])

    ax1.set_zlim(0, 3000)    
    ax1.scatter3D(x, y, z, c=tmp ,marker='o')


if __name__ == "__main__":
    
    serialPort = serial.Serial(port="COM5", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    com_fifo = Queue()

    get_values_thread = Thread(target=read_values, args=(serialPort, com_fifo, ))
    get_values_thread.start()

    style.use('fivethirtyeight')

    fig = plt.figure()
    ax1 = fig.add_subplot(projection='3d')


    ani = animation.FuncAnimation(fig, animate, interval=50)
    plt.show()

    

