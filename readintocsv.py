import smbus
import time
import math

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

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
	
def store_data(accl_scaled_x, accl_scaled_y, accl_scaled_z, gyro_scaled_x, gyro_scaled_y, gyro_scaled_z):
    append = [accl_scaled_x, accl_scaled_y, accl_scaled_z, gyro_scaled_x, gyro_scaled_y, gyro_scaled_z]
    with open("/home/required path/sensor_data.csv", "a") as sensordata:
        writer = csv.writer(sensordata)
        writer.writerow(append)
    sensordata.close()

if __name__ == "__main__":
	bus = smbus.SMBus(2) 	# or bus = smbus.SMBus(0) for older version boards

	Device_Address = 0x68   # MPU6050 device address

	MPU_Init()
	
	

	for i in range(500):
		read_all()
		
		store_data(accl_scaled_x, accl_scaled_y, accl_scaled_z, gyro_scaled_x, gyro_scaled_y, gyro_scaled_z)
		
		
		
		
		
		
		
		
	
