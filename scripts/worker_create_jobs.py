import mysql.connector
import hashlib
import random
from datetime import datetime
from termcolor import colored

db_config = {
    'host': '10.200.1.91',
    'user': 'admin',
    'password': 'admin',
    'database': 'bbt'
}

def log_positive(message):
    print(colored(f" [+] {message}", 'green'))

def log_error(message):
    print(colored(f" [-] {message}", 'red'))

def get_current_utc_time():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def insert_job_status(cursor, connection, job_id, status_message):
    try:
        job_status_insert_query = "INSERT INTO tbl_job_status (job_id, job_update_status, job_date_last_updated) VALUES (%s, %s, %s)"
        job_status_insert_values = (job_id, status_message, get_current_utc_time())
        cursor.execute(job_status_insert_query, job_status_insert_values)
        connection.commit()
        print("Job status inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()


try:
    # Connect to the database
    log_positive("Connecting to Database")
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    # Query to get maxJobQueueSize
    cursor.execute("SELECT max_job_queue_size FROM tbl_job_config WHERE id = 1")
    result = cursor.fetchone()
    if not result:
        raise Exception("No configuration found with id = 1")
    maxJobQueueSize = result['max_job_queue_size']
    log_positive(f"MAX Queue Size: {maxJobQueueSize}")
    # Check if tbl_job_queue exists, if not, create it
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tbl_job_queue (
        job_id VARCHAR(256),
        job_type VARCHAR(256),
        job_category VARCHAR(256),
        geoname_id VARCHAR(256),
        job_target VARCHAR(256),
        job_created_date DATETIME
    )
    """)
    # Check the number of rows in tbl_job_queue
    cursor.execute("SELECT COUNT(*) AS job_count FROM tbl_job_queue")
    job_count = cursor.fetchone()['job_count']
    log_positive(f"Current Jobs in Queue: {job_count}")
    numberOfJobsNeeded = maxJobQueueSize - job_count
    log_positive(f"Adding Jobs to Queue: {numberOfJobsNeeded}")
    if job_count < maxJobQueueSize:
        # Query to get jobs from tbl_city_blocks_ipv4
        cursor.execute(f"""
        SELECT * FROM tbl_city_blocks_ipv4
        WHERE scans_masscan = (
            SELECT LEAST(
                MIN(scans_nmap),
                MIN(scans_masscan)
            )
            FROM tbl_city_blocks_ipv4
        )
        ORDER BY RAND()
        LIMIT {numberOfJobsNeeded};
        """)
        jobs = cursor.fetchall()
        # Check if any jobs were returned
        if not jobs:
            raise Exception(" [-] No jobs found matching the criteria in tbl_city_blocks_ipv4")
        # Insert jobs into tbl_job_queue
        for job in jobs:
            geoname_id = job['geoname_id']
            job_target = job['network']
            job_created_date = get_current_utc_time()
            # Insert masscan row
            job_id = hashlib.sha1(str(random.random()).encode()).hexdigest()
            insert_job_status(cursor, connection, job_id, f"MASSCAN Job Created for Network: {job_target}")
            log_positive(f"Adding MASSCAN Jobs for: {job_target}")
            cursor.execute("""
            INSERT INTO tbl_job_queue (job_id, job_type, job_category, geoname_id, job_target, job_created_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                job_id,
                'masscan_tcp_top3328',
                'masscan',
                geoname_id,
                job_target,
                job_created_date
            ))
            # Insert nmap row
            job_id = hashlib.sha1(str(random.random()).encode()).hexdigest()
            insert_job_status(cursor, connection, job_id, f"NMAP Job Created for Network: {job_target}")
            log_positive(f"Adding MASSCAN Jobs for: {job_target}")
            cursor.execute("""
            INSERT INTO tbl_job_queue (job_id, job_type, job_category, geoname_id, job_target, job_created_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                job_id,
                'nmap_tcp_top3328',
                'nmap',
                geoname_id,
                job_target,
                job_created_date
            ))
        # Commit the transaction
        connection.commit()
        #log_positive("Jobs successfully added to tbl_job_queue")
    else:
        log_positive("Job queue is already at or above the maximum size")
except mysql.connector.Error as err:
    log_error(f"MySQL error: {err}")
except Exception as e:
    log_error(f"Unexpected error: {e}")
finally:
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    except Exception as e:
        log_error(f"Error closing the database connection: {e}")
