import asyncio
import struct
from bleak import BleakClient
from time import sleep


async def acc_handler(sender: int, data: bytearray):
    ax, ay, az, gx, gy, gz = struct.unpack('<ffffff', data)
    print(f"Acc: {ax:0.4f} {ay:0.4f} {az:0.4f} {gx:0.4f} {gy:0.4f} {gz:0.4f}")
# async def gyro_handler(sender: int, data: bytearray):
#     gx, gy, gz = struct.unpack('<fff', data)
#     print(f"Gyro: {gx:0.4f} {gy:0.4f} {gz:0.4f} ")
async def run(address, acc_uuid, gyro_uuid):
    async with BleakClient(address, bufferred= True) as client:
        while True:
            try:
                # Read data from the specified service and characteristic
                # data = []
                # for i in range(0, 10):
                #     acc_rdg = await client.read_gatt_char(acc_uuid)
                #     gyro_rdg = await client.read_gatt_char(gyro_uuid)
                #     ax, ay, az = struct.unpack('<fff', acc_rdg)  
                #     gx, gy, gz = struct.unpack('<fff', gyro_rdg)
                #     data.append(f"{ax:0.4f} {ay:0.4f} {az:0.4f} {gx:0.4f} {gy:0.4f} {gz:0.4f}")
                # # print(f"{ax:0.4f} {ay:0.4f} {az:0.4f} {gx:0.4f} {gy:0.4f} {gz:0.4f}")
                # for i in range(0, 10):
                #     print(data[i]); sleep(0.1)
                await client.start_notify(acc_uuid, acc_handler)
                # await client.start_notify(gyro_uuid, gyro_handler)
            except KeyboardInterrupt:
                break  # Stop the loop on Ctrl+C

if __name__ == "__main__":
    # Replace these values with your specific BLE device's address, service UUID, and characteristic UUID
    device_address = "A7:7E:1B:4D:2B:49"
    service_uuid = "1101"  # Replace with the actual service UUID
    acc_uuid = "00002101-0000-1000-8000-00805f9b34fb"  
    gyro_uuid  = "00002102-0000-1000-8000-00805f9b34fb"
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(device_address, acc_uuid, gyro_uuid))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
