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
            if(len(tmp_values) !=0):
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

    raw_angle = int(values.pop(0)[0])
    angle = (raw_angle)*m.pi/180

    matrice = np.zeros((8,8))
    for i in range(len(values)):
        matrice[int(values[i][0]), int(values[i][1])] = int(values[i][2])

    # Display values with lines from TOF and angle
    x_temp,y_temp,z_temp=0,0,0
    x_rot,y_rot,z_rot=0,0,0

    # Using a rotation matrix to rotate value in space
    for row in range(8):
        for col in range(8):
            index = 8*row + col
            x_temp = (row-4)*m.sin(0.11999)*int(values[index][2])
            y_temp = (col-4)*m.sin(0.11999)*int(values[index][2])
            z_temp = int(values[index][2])

            x_rot = m.cos(angle)*x_temp - m.sin(angle)*z_temp
            y_rot = y_temp
            z_rot = m.sin(angle)*x_temp + m.cos(angle)*z_temp

            x.append(x_rot)
            y.append(y_rot)
            z.append(z_rot)

    # Display
    ax1.clear()
    ax1.set_xlim(-1000, 1000)    
    ax1.set_ylim(-1000, 1000)   
    ax1.set_zlim(0, 2000) 
    ax1.scatter3D(x, y, z, marker='o')

if __name__ == "__main__":
    
    x = []
    y = []
    z = []

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

    

