import pymysql

localhost = "127.0.0.1"
user = "root"
database = "emhart"

connection = pymysql.connect(host=localhost,
                             user=user,
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS Emhart")
        cursor.execute("USE Emhart")
        
        # Create devices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mac_address VARCHAR(255) NOT NULL UNIQUE
            )
        """)
        
        # Create Measurements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Measurements (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                DeviceID INT,
                Temperature FLOAT,
                Humidity FLOAT,
                Log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (DeviceID) REFERENCES devices(id)
            )
        """)
        
    connection.commit()
finally:
    connection.close()

print("Database and tables created successfully.")