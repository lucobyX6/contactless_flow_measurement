# - - - Librairies - - -

# Data transmission
import serial
from queue import Queue
from threading import Thread

# List handler
import numpy as np

# Show results
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

# Mathematical formula
import math as m

# Delay
from time import sleep

def read_values(serialPort : serial, com_fifo : Queue):
    """
    **Abstract** : Read formatted values from STM32 board, store it in a list and send it through a pipe

    **Input** :
    - serialPort [serial] : Connection to reading port
    - com_fifo [Queue] : Pipe to transmit data in a list to animate

    **Output** : None

    **Indirect output** : com_fifo pipe

    **Necessary librairies** :
    - import serial 
    - from queue import Queue
    - from threading import Thread
    """
    
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
    """
    **Abstract** : Display with 50ms loop values on a 3D graph 

    **Input** :
    - i [int]

    **Output** : None

    **Indirect output** : None

    **Necessary librairies** :
    - import numpy as np
    - import math as m
    - import matplotlib.pyplot as plt
    - import matplotlib.animation as animation
    - from matplotlib import style
    - 
    """
    
    # Get values (distances, objects)  
    values = com_fifo.get()
    
    # Transform list in corresponding matrice
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

    # Define color for objects
    color = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]
    tmp = []
    for i in range(len(matrice_objects)):
        for j in range(len(matrice_objects)):
            index = int(matrice_objects[i][j])
            if(index >= len(color)):
                index = index%len(color)
            tmp.append(color[index])
    
    # Display values
    x = []
    y = []
    z = []

    for i in range(len(matrice_distances)):
        for j in range(len(matrice_distances[0])):
            x.append(i)
            y.append(j)
            z.append(matrice_distances[i][j])

    ax1.clear()  
    ax1.set_zlim(0, 3000)    
    ax1.scatter3D(x, y, z, c=tmp ,marker='o')


if __name__ == "__main__":
    
    # Turn on connection with board
    serialPort = serial.Serial(port="COM5", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    # Fifo to transmit from read_values to animate
    com_fifo = Queue()

    # Get values
    get_values_thread = Thread(target=read_values, args=(serialPort, com_fifo, ))
    get_values_thread.start()

    # Display values on 3D chart
    style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(projection='3d')
    ani = animation.FuncAnimation(fig, animate, interval=50)
    plt.show()

    

