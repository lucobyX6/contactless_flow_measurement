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
    
    threshold = 500 # Threshold to be a neighbor
    
    group = 1 # Group counter
    find = False # If no group in neighborhood, define a arbitrary group

    # Get values (distances, objects)  
    values = com_fifo.get()

    angle = int(values.pop(0)[0][0])
    print(angle)

    matrice = np.zeros((8,8))
    for i in range(len(values)):
        matrice[int(values[i][0]), int(values[i][1])] = int(values[i][2])

    matrice_objects = np.zeros((8,8))

    # Calculate objects
    diff = np.zeros((3,3))

    for row in range(len(matrice)):
        for col in range(len(matrice[0])):
            
            # A point is in neighborhood (threshold) ? 
            if(row-1 < 0 or col-1 < 0):
                diff[0][0] = 9999 
            else:
                diff[0][0] = np.abs(matrice[row][col] - matrice[row-1][col-1])

            if(row-1 < 0):
                diff[0][1] = 9999
            else:
                diff[0][1] = np.abs(matrice[row][col] - matrice[row-1][col])

            if(row-1 < 0 or col+1 > len(matrice[0])-1):
                diff[0][2] = 9999
            else:
                diff[0][2] = np.abs(matrice[row][col] - matrice[row-1][col+1])

            if(col-1 < 0):
                diff[1][0] = 9999
            else:
                diff[1][0] = np.abs(matrice[row][col] - matrice[row][col-1])

            diff[1][1] = -1

            if(col+1 > len(matrice[0])-1):
                diff[1][2] = 9999
            else:
                diff[1][2] = np.abs(matrice[row][col] - matrice[row][col+1])

            if(row+1 > len(matrice)-1 or col-1 < 0):
                diff[2][0] = 9999
            else:
                diff[2][0] = np.abs(matrice[row][col] - matrice[row+1][col-1])

            if(row+1 > len(matrice)-1):
                diff[2][1] = 9999
            else:
                diff[2][1] = np.abs(matrice[row][col] - matrice[row+1][col])

            if(row+1 > len(matrice[0])-1 or col+1 > len(matrice)-1):
                diff[2][2] = 9999
            else:
                diff[2][2] = np.abs(matrice[row][col] - matrice[row+1][col+1])

            # This neighbor has a group ? 
            for i in range(len(diff)):
                for j in range(len(diff[0])):
                    value = diff[i][j]
                    if((value != 9999 and value !=-1) and value < threshold): 
                        if(matrice_objects[row+i-1][col+j-1] !=0):
                            matrice_objects[row][col] = matrice_objects[row+i-1][col+j-1]
                            find = True

            # If no, assign an arbitrary group       
            if(find == False):
                matrice_objects[row][col] = group
                group +=1
            else:
                find = False
    
    # Define a color for a group
    color = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]
    tmp = []
    for i in range(len(matrice_objects)):
        for j in range(len(matrice_objects)):
            index = int(matrice_objects[i][j])
            if(index >= len(color)):
                index = index%len(color)
            tmp.append(color[index])
    
    # Display values with lines from TOF and angle
    origin = [0,0]
    x_temp,y_temp,z_temp=0,0,0
    x_rot,y_rot,z_rot=0,0,0

    x = []
    y = []
    z = []

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

    ax1.clear()
    ax1.set_xlim(-1000, 1000)    
    ax1.set_ylim(-1000, 1000)    
    for i in range(len(z)):
        ax1.plot([origin[0], x[i]], [origin[0], y[i]], zs = [0, z[i]], linewidth=1, color = 'blue', alpha=0.1)
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

    

