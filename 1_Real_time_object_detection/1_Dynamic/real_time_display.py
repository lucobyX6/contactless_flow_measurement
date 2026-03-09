import serial
from queue import Queue
from threading import Thread
import numpy as np

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
            com_fifo.put(tmp_values)

        if(reading == True and "start" not in serialString):
            tmp_values.append(serialString[:-1].split(","))

def animate(i):
    values = com_fifo.get()
    matrice = np.zeros((len(values),len(values)))

    ax1.clear()

    for i in range(len(values)):
        matrice[int(values[i][0]), int(values[i][1])] = int(values[i][2])
    
    #ax1.matshow(matrice)
    ax1.set_zlim(0, 3000)
    ax1.scatter3D([int(values[i][0]) for i in range(len(values))], [int(values[i][1]) for i in range(len(values))], [int(values[i][2]) for i in range(len(values))], color='red', marker='o')

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

    

