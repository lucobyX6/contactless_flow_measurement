import serial
from queue import Queue
from threading import Thread
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import math as m

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
            com_fifo.put(tmp_values)

        if(reading == True and "start" not in serialString):
            tmp_values.append(serialString[:-1].split(","))

        if("rotation" in serialString):
            print("rotation")
    
if __name__ == "__main__":
    
    serialPort = serial.Serial(port="COM5", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    com_fifo = Queue()

    get_values_thread = Thread(target=read_values, args=(serialPort, com_fifo, ))
    get_values_thread.start()

    style.use('fivethirtyeight')

    fig = plt.figure()
    ax1 = fig.add_subplot(projection='3d')

    matrice = np.zeros((8,8))
    
    values = com_fifo.get()

    for i in range(len(values)):
        matrice[int(values[i][0]), int(values[i][1])] = int(values[i][2])

    x = []
    y = []
    z = []

    for row in range(8):
        for col in range(8):
            index = 8*row + col
            x.append((row-4)*m.sin(0.11999)*int(values[index][2]))
            y.append((col-4)*m.sin(0.11999)*int(values[index][2]))
            z.append(int(values[index][2]))

    print(x)
    print(y)

    ax1.scatter3D(x, y, z, color='red', marker='o')


    # values = com_fifo.get()

    # for i in range(len(values)):
    #     matrice[int(values[i][0]), int(values[i][1])] = int(values[i][2])
    
    # ax1.scatter3D([int(values[i][0]) for i in range(len(values))], [int(values[i][2]) for i in range(len(values))], [int(values[i][1]) for i in range(len(values))], color='red', marker='o')

    plt.show()

    

