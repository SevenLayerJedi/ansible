import csv
import mysql.connector
from mysql.connector import Error
import zipfile

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
            CREATE TABLE IF NOT EXISTS city_locations_en (
                geoname_id INT,
                locale_code VARCHAR(255),
                continent_code VARCHAR(255),
                continent_name VARCHAR(255),
                country_iso_code VARCHAR(255),
                country_name VARCHAR(255),
                subdivision_1_iso_code VARCHAR(255),
                subdivision_1_name VARCHAR(255),
                subdivision_2_iso_code VARCHAR(255),
                subdivision_2_name VARCHAR(255),
                city_name VARCHAR(255),
                metro_code VARCHAR(255),
                time_zone VARCHAR(255),
                is_in_european_union BOOLEAN
            );
        """)
        print("Table created successfully.")
        conn.commit()
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def import_csv_to_mysql(conn, zip_filepath, csv_filename):
    try:
        cursor = conn.cursor()
        with zipfile.ZipFile(zip_filepath) as z:
            with z.open(csv_filename) as file:
                reader = csv.reader(line.decode('utf-8') for line in file)
                next(reader)  # Skip the header row
                for row in reader:
                    cursor.execute("""
                        INSERT INTO city_locations_en (geoname_id, locale_code, continent_code, continent_name, country_iso_code, country_name, subdivision_1_iso_code, subdivision_1_name, subdivision_2_iso_code, subdivision_2_name, city_name, metro_code, time_zone, is_in_european_union)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, row)
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
        zip_filepath = '/opt/ansible/geoip/GeoLite2-City-Locations-en.csv.zip'
        csv_filename = 'GeoLite2-City-Locations-en.csv'
        import_csv_to_mysql(conn, zip_filepath, csv_filename)
        conn.close()

if __name__ == '__main__':
    main()

