import serial
import pymysql
import json
import re
import numpy as np


localhost = "127.0.0.1"
user = "root"
database = "emhart"

connection = pymysql.connect(host=localhost,
                             user=user,
                             cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
    ser = serial.Serial(port='COM3', baudrate=115200, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            json_received = ser.readline().decode('latin-1').rstrip()
            print("json0 :", json_received)

            if "id" in json_received:
                print("correct data")
                jsonData = json_received[json_received.find('{"id"'):]
                print("json1 :", jsonData)
                jsonR = json.loads(jsonData)
                print("json2 :", jsonR)

                ID = jsonR["id"]
                MAC = ID
                T = jsonR["t"]
                H = jsonR["h"]
                print("json:", jsonData)
                print("ID:", ID)
                print("T:", T)
                print("H:", H)
            else:
                print("Not correct data")

            with connection.cursor() as cursor:
                # Check if device exists
                sql = "SELECT `id` FROM `devices` WHERE `mac_address`=%s"
                cursor.execute(sql, (ID,))
                result = cursor.fetchone()

                if result:
                    deviceID = result["id"]
                else:
                    # Insert new device
                    sql = "INSERT INTO `devices` (`mac_address`) VALUES (%s)"
                    cursor.execute(sql, (ID,))
                    connection.commit()
                    deviceID = cursor.lastrowid

                print(deviceID)

            with connection.cursor() as cursor:
                sql = "INSERT INTO `Measurements` (`DeviceID`, `Temperature`, `Humidity`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (deviceID, T, H))

            connection.commit()

            with connection.cursor() as cursor:
                sql = "SELECT `ID`, `Temperature`, `Humidity`, `Log_time` FROM `Measurements` WHERE `DeviceID`=%s"
                cursor.execute(sql, (deviceID,))
                result = cursor.fetchall()

                for row in result:
                    print(row)
                    print("ID = ", row["ID"])
                    print("Temp = ", row["Temperature"])
                    print("Hum = ", row["Humidity"])
                    print("ID = ", MAC)
                    print("Time = ", row["Log_time"])