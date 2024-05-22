import pymysql
import hashlib
import random
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Database configuration
db_config = {
    'host': '10.200.1.91',
    'user': 'admin',
    'password': 'admin',
    'database': 'bbt'
}

# Connect to MySQL database
try:
    connection = pymysql.connect(host=db_config['host'],
                                 user=db_config['user'],
                                 password=db_config['password'],
                                 database=db_config['database'])
    print(Fore.GREEN + "  [+] Connected to the database successfully")
except pymysql.MySQLError as e:
    print(Fore.RED + f"  [-] Error connecting to MySQL Database: {e}")
    exit(1)

try:
    with connection.cursor() as cursor:
        # Get the max number of jobs that can be in the queue
        try:
            cursor.execute("SELECT max_job_queue_size FROM tbl_job_config")
            jobsInQueueMaxSize = cursor.fetchone()[0]
            print(Fore.GREEN + f"  [+] Max queue job size retrieved: {jobsInQueueMaxSize}")
        except pymysql.MySQLError as e:
            print(Fore.RED + f"  [-] Error fetching max queue job size: {e}")
            raise
        #
        # Get the current number of jobs in the queue
        try:
            cursor.execute("SELECT COUNT(*) FROM tbl_job_queue")
            jobsInQueue = cursor.fetchone()[0]
            print(Fore.GREEN + f"  [+] Current number of jobs in the queue: {jobsInQueue}")
        except pymysql.MySQLError as e:
            print(Fore.RED + f"  [-] Error counting jobs in queue: {e}")
            raise
        #
        # Calculate jobsCountNeeded
        jobsCountNeeded = jobsInQueueMaxSize - jobsInQueue
        addJobs = jobsInQueue < jobsInQueueMaxSize

        # If jobs can be added
        if addJobs and jobsCountNeeded > 0:
            try:
                # Query for the city locations with the minimum total scans
                cursor.execute("""
                SELECT geoname_id
                FROM tbl_city_locations_en
                WHERE country_iso_code = 'US' AND
                      subdivision_1_iso_code = 'CO' AND
                      total_scans = (SELECT MIN(total_scans) FROM tbl_city_locations_en)
                ORDER BY RAND()
                LIMIT %s;
                """, (jobsCountNeeded,))
                geoNameIds = cursor.fetchall()
                print(Fore.GREEN + f"  [+] GeoName IDs fetched for processing: {len(geoNameIds)} locations")
            except pymysql.MySQLError as e:
                print(Fore.RED + f"  [-] Error fetching geoNameIds: {e}")
                raise
            # For each location, find networks and create jobs
            for geoname_id in geoNameIds:
                try:
                    cursor.execute("""
                    SELECT network
                    FROM tbl_city_blocks_ipv4
                    WHERE geoname_id = %s
                    """, (geoname_id,))
                    networks = cursor.fetchall()
                    print(Fore.GREEN + f"  [+] Networks fetched for GeoName ID {geoname_id}: {len(networks)} networks")
                except pymysql.MySQLError as e:
                    print(Fore.RED + f"  [-] Error fetching networks: {e}")
                    continue
                for network in networks:
                    # Generate a random SHA1 hash for the job_id
                    job_id = hashlib.sha1(str(random.random()).encode()).hexdigest()
                    # Insert job into the job queue
                    try:
                        cursor.execute("""
                        INSERT INTO tbl_job_queue (job_id, job_type, job_category, geoname_id, job_target, job_created_date)
                        VALUES (%s, 'nmap_full_tcp', 'nmap', %s, %s, %s)
                        """, (job_id, geoname_id, network[0], datetime.utcnow()))
                        print(Fore.GREEN + f"  [+] Job created successfully: {job_id}")
                        #
                        # Also insert into tbl_job_status
                        cursor.execute("""
                        INSERT INTO tbl_job_status (job_id, job_update_status, job_date_last_updated)
                        VALUES (%s, 'Added Job to Job Queue', %s)
                        """, (job_id, datetime.utcnow()))
                        print(Fore.GREEN + f"  [+] Job status updated successfully for {job_id}")
                    except pymysql.MySQLError as e:
                        print(Fore.RED + f"  [-] Error inserting job into queue: {e}")
                        continue
            connection.commit()
except Exception as e:
    print(Fore.RED + f"  [-] An error occurred: {e}")
    connection.rollback()
finally:
    connection.close()
    print(Fore.GREEN + "  [+] Connection closed successfully")
