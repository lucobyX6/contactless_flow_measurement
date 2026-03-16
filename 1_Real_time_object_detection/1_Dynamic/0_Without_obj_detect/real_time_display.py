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

# - - - Function - - -

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
            com_fifo.put(tmp_values)

        if(reading == True and "start" not in serialString):
            tmp_values.append(serialString[:-1].split(","))


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
    
    # Get values
    values = com_fifo.get()
    
    # Display values with scatter
    ax1.clear()
    ax1.set_zlim(0, 3000)
    ax1.scatter3D([int(values[i][0]) for i in range(len(values))], [int(values[i][1]) for i in range(len(values))], [int(values[i][2]) for i in range(len(values))], color='red', marker='o')


# - - - Main - - -

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

    

