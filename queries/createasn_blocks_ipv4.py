import pandas as pd
import mysql.connector
from mysql.connector import Error
import zipfile
import io

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='10.200.1.91',
            user='admin',
            password='admin',
            database='bbt'
        )
        if conn.is_connected():
            print("Connected to the database successfully.")
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tbl_asn_blocks_ipv4 (
                network VARCHAR(255),
                autonomous_system_number INT,
                autonomous_system_organization VARCHAR(255)
            );
        """)
        conn.commit()
        print("Table created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def import_csv_to_mysql(conn, zip_filepath, csv_filename):
    try:
        cursor = conn.cursor()
        with zipfile.ZipFile(zip_filepath) as z:
            with z.open(csv_filename) as file:
                df = pd.read_csv(io.TextIOWrapper(file, 'utf-8'))
                for index, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO tbl_asn_blocks_ipv4 (network, autonomous_system_number, autonomous_system_organization)
                        VALUES (%s, %s, %s);
                    """, tuple(row))
                conn.commit()
                print("Data imported successfully.")
    except Error as e:
        print(f"Error importing data: {e}")
    finally:
        cursor.close()

def main():
    conn = connect_to_database()
    if conn and conn.is_connected():
        create_table(conn)
        zip_filepath = '/opt/geoip/GeoLite2-ASN-Blocks-IPv4.csv.zip'
        csv_filename = 'GeoLite2-ASN-Blocks-IPv4.csv'
        import_csv_to_mysql(conn, zip_filepath, csv_filename)
        conn.close()

if __name__ == '__main__':
    main()
