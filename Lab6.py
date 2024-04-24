# Author: Mingqi Li
# Date: 2024/04/18
# Purpose: Plot the ADC reading X and Y channels in real time
# GUI Guide:
#   1. Change COM_PORT in this code, and start the python code
#   2. Start the C code and start sending data
#   3. Press Plot button on the GUI
#   4. After plotting done, can re-send data from C code, 
#       and press plot again will plot the new graph
#   5. Uart reading 2 bytes a time, and LITTLE Endian

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import datetime
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BAUDRATE = 19200
COM_PORT = 'COM5'       # change this to your COM_PORT
CPU_FREQ = 1.048*10**6
CPU_CLK = 1/CPU_FREQ
SAMP_FREQ = 60

try:
    ser = serial.Serial(port= COM_PORT,
                        baudrate=BAUDRATE,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1)
    if ser.is_open:
        print("port connected!")
except IOError:
    print("Failed at setting port\n")


t_max = 10000 # in ms
samp_period = 1000/SAMP_FREQ # in ms
vol_max = 4096



class __lab6_plot(ttk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master

        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Lab 6 Sensor")
        self.ax.set_xlabel("time, ms")
        self.ax.set_ylabel("voltage, V")

        self.testCanvas = FigureCanvasTkAgg(self.fig, self.master)
        self.testCanvas.get_tk_widget().place(
                                    relx=0.5,
                                    rely=0.5,
                                    anchor='center',
                                    relwidth=1,
                                    relheight=1)
               
        self.ax.set_xlim(0,t_max)
        self.ax.set_ylim(0, 1.1*vol_max)

        style1 = ttk.Style()
        style1.configure('Button1.TButton', font=('Helvetica', 26))
        Button1 = ttk.Button(self.master,text='Plot',command=self.__get_data)
        Button1.place(relx=0,rely=0,relheight=0.05,relwidth=0.2)

        style2 = ttk.Style()
        style2.configure('Button2.TButton', font=('Helvetica', 26))
        Button2 = ttk.Button(self.master,text='Flush Input',command=self.__flush_input)
        Button2.place(relx=0,rely=0.05,relheight=0.05,relwidth=0.2)


    def __get_data(self):
        self.fig.legends=[] 
        self.ax.cla() 
               
        self.ax.set_xlim(0,t_max)
        self.ax.set_ylim(0, 1.1*vol_max)

        adc_Xdata = []
        adc_Ydata = []
        t=[]
        count = 0

        self.lineX, = self.ax.plot([], [], label='X rotation')
        self.lineY, = self.ax.plot([], [], label='Y rotation')
        self.fig.legend()

        x_flag = True
        y_flag = False
        while ser.in_waiting:
            new_data = int.from_bytes(ser.read(2),byteorder='little')
            
            if x_flag:
                adc_Xdata.append(new_data)
                print("x data: ", new_data)
                t.append(count*samp_period)
                count += 1
                x_flag = False
                y_flag = True

            elif y_flag:
                adc_Ydata.append(new_data)
                print("y data: ", new_data)

                x_flag = True
                y_flag = False

                self.lineX.set_data(t, adc_Xdata)
                self.lineY.set_data(t, adc_Ydata)
                self.testCanvas.draw()
                root.update()

                # time.sleep(0.001)

    def __flush_input(self):
        ser.reset_input_buffer()

root = tk.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}+0+0")
app = __lab6_plot(master=root)
root.mainloop()
ser.close()





# line1, = ax.plot([], [], lw=2)
# # line2, = ax.plot([], [], lw=2)

# while i<num_samp:
#     newX_data = int.from_bytes(ser.read(2),byteorder='little')
#     adc_Xdata.append(newX_data)
#     print(newX_data)
#     i = len(adc_Xdata)
#     plt.plot(t[:i],adc_Xdata)

# def init():
#     ax.set_xlim(0,t_max)
#     ax.set_ylim(0, 1.1*vol_max)
#     return line1,

# def update(frame):
#         newX_data = int.from_bytes(ser.read(2),byteorder='little')
#         adc_Xdata.append(newX_data)
#         print(newX_data)
#         t.append(frame)
#         line1.set_data(t, adc_Xdata)  # X-axis
#         return line1,


# # Generate data and update the plot continuously
# ani = FuncAnimation(fig, update, frames=np.linspace(0, t_max, int(num_samp)),
#                     init_func=init, blit=True)
