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

def read_values(serial_port : serial, com_fifo : Queue):
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
        serial_string = str(serial_port.readline().decode("Ascii"))

        if("start" in serial_string):
            reading = True
            tmp_values = []
        
        if("end" in serial_string):
            reading = False
            com_fifo.put(tmp_values)

        if(reading == True and "start" not in serial_string):
            tmp_values.append(serial_string[:-1].split(","))

        if("rotation" in serial_string):
            print("rotation")
    
if __name__ == "__main__":
    
    serial_port = serial.Serial(port="COM5", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    com_fifo = Queue()

    get_values_thread = Thread(target=read_values, args=(serial_port, com_fifo, ))
    get_values_thread.start()

    style.use('fivethirtyeight')

    fig = plt.figure()
    ax1 = fig.add_subplot(projection='3d')

    matrice = np.zeros((8,8))
    
    values = com_fifo.get()

    for i in range(len(values)):
        matrice[int(values[i][0]), int(values[i][1])] = int(values[i][2])

    x_temp,y_temp, z_temp=0,0,0
    x_rot,y_rot, z_rot=0,0,0

    x = []
    y = []
    z = []

    angle = 0

    for row in range(8):
        for col in range(8):
            index = 8*row + col
            x_temp = (row-4)*m.sin(0.11999)*int(values[index][2])
            y_temp = (col-4)*m.sin(0.11999)*int(values[index][2])
            z_temp = (values[index][2])

            x_rot = m.cos(angle)*x_temp - m.sin(angle)*z_temp
            y_rot = y_temp
            z_rot = m.sin(angle)*x_temp + m.cos(angle)*z_temp

            x.append(x_rot)
            y.append(y_rot)
            z.append(z_rot)

    ax1.scatter3D(x, y, z, color='red', marker='o')


    # values = com_fifo.get()

    # for i in range(len(values)):
    #     matrice[int(values[i][0]), int(values[i][1])] = int(values[i][2])
    
    # ax1.scatter3D([int(values[i][0]) for i in range(len(values))], [int(values[i][2]) for i in range(len(values))], [int(values[i][1]) for i in range(len(values))], color='red', marker='o')

    plt.show()

    

