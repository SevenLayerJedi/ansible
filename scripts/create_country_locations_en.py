import pandas as pd
import mysql.connector
from mysql.connector import Error
import zipfile
import io

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='10.200.1.91',  # Adjust as necessary
            user='admin',        # Adjust as necessary
            password='admin',    # Adjust as necessary
            database='bbt'       # Adjust as necessary
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
            CREATE TABLE IF NOT EXISTS tbl_country_locations_en (
                geoname_id INT,
                locale_code VARCHAR(2),
                continent_code VARCHAR(2),
                continent_name VARCHAR(255),
                country_iso_code VARCHAR(2),
                country_name VARCHAR(255),
                is_in_european_union BOOLEAN
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
                        INSERT INTO tbl_country_locations_en (geoname_id, locale_code, continent_code, continent_name, country_iso_code, country_name, is_in_european_union)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
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
        zip_filepath = '/opt/geoip/GeoLite2-Country-Locations-en.csv.zip'
        csv_filename = 'GeoLite2-Country-Locations-en.csv'
        import_csv_to_mysql(conn, zip_filepath, csv_filename)
        conn.close()

if __name__ == '__main__':
    main()
