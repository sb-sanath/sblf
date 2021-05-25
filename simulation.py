import smbus
import time
import math
import numpy as np
import matplotlib.pyplot as plt

figure, axis = plt.subplots(2, 2)

x_axis_values = 0
accl_scaled_x = 0
accl_scaled_y = 0
accl_scaled_z = 0
gyro_scaled_x = 0
gyro_scaled_y = 0
gyro_scaled_z = 0

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)
	

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

def read_all():
	acclX = read_raw_data(ACCEL_XOUT_H)
	acclY = read_raw_data(ACCEL_YOUT_H)
	acclZ = read_raw_data(ACCEL_ZOUT_H)

	gyroX = read_raw_data(GYRO_XOUT_H)
	gyroY = read_raw_data(GYRO_YOUT_H)
	gyroz = read_raw_data(GYRO_ZOUT_H)


	accl_scaled_x = acclX / 16384.0
	accl_scaled_y = acclY / 16384.0
	accl_scaled_z = acclZ / 16384.0

	gyro_scaled_x = gyroX/131.0
	gyro_scaled_y = gyroY/131.0
	gyro_scaled_z = gyroZ/131.0
	x_axis_values = x_axis_values +1
	
if __name__ == "__main__:
	xaxis = []
	accl_x = []
	accl_y = []
	accl_z = []
	gyro_x = []
	gyro_y = []
	gyro_z = []
	
	bus = smbus.SMBus(2) 	# or bus = smbus.SMBus(0) for older version boards

	Device_Address = 0x68   # MPU6050 device address

	MPU_Init()
	
	for i in range (500):
	
		read_all()

		xaxis.append(x_axis_values)

		accl_x.append(accl_scaled_x)
		accl_y.append(accl_scaled_y)
		accl_z.append(accl_scaled_z)

		gyro_x.append(gyro_scaled_x)
		gyro_y.append(gyro_scaled_y)
		gyro_z.append(gyro_scaled_z)
		 
		#plt.axis([0,10,0,1])
		x=np.array(xaxis)

		y1 = np.array(accl_x)
		y2 = np.array(accl_y)
		y3 = np.array(accl_z)

		y4 = np.array(gyro_x)
		y5 = np.array(gyro_y)
		y6 = np.array(gyro_z)
		#y2 = np.cos(x)
		#y=np.arange(0,10,1) ##to print line at 0
		#plt.plot(x,y1)
		#plt.plot(x,y2)
		#axis.axhline(y=0)
		axis[0,0].plot(x,y1)
		axis[0,0].plot(x,y2)
		axis[0,0].plot(x,y3)
		axis[0,0].set_title("accelerometer")

		axis[0,1].plot(x,y4)
		axis[0,1].plot(x,y5)
		axis[0,1].plot(x,y6)
		axis[0,1].set_title("gyroscope")
	
	
	#axis[0,0].plot(x,(y1-x)) #to print line at 0
	
	plt.show()


 
