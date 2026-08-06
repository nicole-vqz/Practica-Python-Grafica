import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import serial
import time

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
muestra = None
muestran = None
muestraa = None
limi = None
lims = None
dif = None
# Initialize communication with serial port
print('conectando serial...')
arduino=serial.Serial('COM6',9600, timeout = 3.0)
print('conectado.')

limi = int(input("Ingrese el valor mínimo del rango: "))
lims = int(input("Ingrese el valor máximo del rango: "))
dif = int(lims - limi)
# This function is called periodically from FuncAnimation
def animate(i, xs, ys, muestra):

	# Read sample from serial port
	arduino.write('r'.encode())
	if arduino.inWaiting() > 0:
		#sig = int(arduino.readline().strip())
		#sig = float(arduino.readline().strip())
		muestra = arduino.readline().strip()
		if not muestra:
			return
		muestra = int(muestra)
		muestran = float(muestra/4095)
		muestraa = float((muestran * dif)+limi)
		#muestra = float(muestra)
		#print(muestra)

		# Add x and y to lists
		xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
		ys.append(muestraa)


		# Limit x and y lists to 20 items
		xs = xs[-20:]
		ys = ys[-20:]

		# Draw x and y lists
		ax.clear()
		ax.plot(xs, ys)

		# Format plot
		plt.xticks(rotation=45)
		plt.subplots_adjust(bottom=0.30)
		plt.title('Leyendo puerto serial')
		plt.ylabel('Amplitud')

# Set up plot to call animate() function periodically
n = 0
while n<2:
	muestra = arduino.readline().strip()
	n+=1
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, muestraa), interval=500)
plt.show()