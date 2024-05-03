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
            CREATE TABLE IF NOT EXISTS tbl_city_blocks_ipv4 (
                network VARCHAR(255),
                geoname_id INT,
                registered_country_geoname_id INT,
                represented_country_geoname_id INT,
                is_anonymous_proxy BOOLEAN,
                is_satellite_provider BOOLEAN,
                postal_code VARCHAR(255),
                latitude DECIMAL(10, 6),
                longitude DECIMAL(10, 6),
                accuracy_radius INT,
                is_anycast BOOLEAN
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
                        INSERT INTO tbl_city_blocks_ipv4 (network, geoname_id, registered_country_geoname_id, represented_country_geoname_id, is_anonymous_proxy, is_satellite_provider, postal_code, latitude, longitude, accuracy_radius, is_anycast)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, tuple(row.fillna(None)))
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
        zip_filepath = '/opt/geoip/GeoLite2-City-Blocks-IPv4.csv.zip'
        csv_filename = 'GeoLite2-City-Blocks-IPv4.csv'
        import_csv_to_mysql(conn, zip_filepath, csv_filename)
        conn.close()

if __name__ == '__main__':
    main()
