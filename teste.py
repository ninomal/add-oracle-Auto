import cx_Oracle

# Update these values with your database information
dsn = 'localhost:1521/XEPDB1'
username = 'ninomal'
password = 'ADMIN'

try:
    # Establish the connection
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    print("Connection successful!")

    # Optional: Run a simple query
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table_name")
    for row in cursor:
        print(row)

except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Error code:", error.code)
    print("Error message:", error.message)

finally:
    # Clean up
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()


