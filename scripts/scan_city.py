import mysql.connector
import subprocess
import hashlib
import random
import datetime
from mysql.connector import Error

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='10.200.1.91',
            user='admin',
            password='admin',
            database='bbt'
        )
        print(" [+] Connected to the database successfully.")
        return conn
    except Error as e:
        print(f" [+] Error connecting to MySQL: {e}")
        return None

def get_geoname_id(conn):
    query = """
    SELECT *
    FROM tbl_city_locations_en
    WHERE country_iso_code = 'US' AND
        subdivision_1_iso_code = 'CO' AND
        total_scans = (
            SELECT MIN(total_scans)
            FROM tbl_city_locations_en
        )
    ORDER BY RAND()
    LIMIT 1;
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    if result:
        print(f" [+] Geoname ID found: {result['geoname_id']}")
    else:
        print(" [+] No rows found with minimum scans.")
    return result['geoname_id'] if result else None

def get_networks(conn, geoname_id):
    query = f"SELECT network FROM tbl_city_blocks_ipv4 WHERE geoname_id = '{geoname_id}'"
    cursor = conn.cursor()
    cursor.execute(query)
    networks = [row[0] for row in cursor.fetchall()]
    print(f" [+] Networks to scan for geoname ID {geoname_id}: {networks}")
    return networks

def update_scan_details(conn, geoname_id):
    current_time = datetime.datetime.now()
    query = """
    UPDATE tbl_city_locations_en
    SET total_scans = total_scans + 1,
        last_scanned_datetime = %s
    WHERE geoname_id = %s;
    """
    cursor = conn.cursor()
    cursor.execute(query, (current_time, geoname_id))
    conn.commit()
    cursor.close()
    print(f" [+] Updated tbl_city_locations_en with new scan details for geoname ID {geoname_id}.")

def generate_job_id():
    job_id = hashlib.sha1(str(random.random()).encode()).hexdigest()
    print(f" [+] Generated job ID: {job_id}")
    return job_id

def run_nmap_scans(networks, geoname_id, job_id):
    for network in networks:
        directory = f"/opt/nmap/{job_id}/{geoname_id}"
        subprocess.run(["mkdir", "-p", directory])
        cmd = f"nmap -sC -sV -oA {directory} -p- --script=banner {network}"
        subprocess.run(cmd, shell=True)
        print(f" [+] Scanned network {network} with results stored in {directory}")

def main():
    conn = connect_to_database()
    if conn:
        geoname_id = get_geoname_id(conn)
        if geoname_id:
            networks = get_networks(conn, geoname_id)
            job_id = generate_job_id()
            run_nmap_scans(networks, geoname_id, job_id)
            update_scan_details(conn, geoname_id)
            # Run the external Python script with fLocation as parameter
            #fLocation = f"/opt/nmap/{job_id}/{geoname_id}"
            #subprocess.run(["python", "import_nmapdata.py", fLocation])
            #print(f" [+] Finished running import_nmapdata with location {fLocation}")
        conn.close()

if __name__ == '__main__':
    main()
