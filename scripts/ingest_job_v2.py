import mysql.connector
import hashlib
import shutil
import subprocess
from datetime import datetime
from termcolor import colored
import os

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

try:
    log_positive(f"Creating MYSQL Cursor")
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    # Look for a job in tbl_job_queue
    log_positive(f"Checking for any jobs in queue")
    cursor.execute((
    "SELECT job_id, job_type, job_category, geoname_id, job_target, job_created_date "
    "FROM tbl_job_queue "
    "ORDER BY job_created_date "
    "LIMIT 1"
    ))
    #log_positive(f"DEBUG 001")
    #for row in cursor:
    #    print(row)
    # {'job_id': '5ae5084935571b4315593a00d83e54e803484899', 'job_type': 'nmap_full_tcp', 'job_category': 'nmap', 'geoname_id': '5574704', 'job_target': '38.109.215.64/26', 'job_created_date': datetime.datetime(2024, 5, 11, 18, 42, 26)}
    job = cursor.fetchone()
    #log_positive(f"DEBUG 002")
    # Check if there are any jobs
    #print(job)
    if not job:
        log_error("No jobs in the queue")
        exit(1)
    #
    #log_positive(f"DEBUG 003")
    #job_id = hashlib.sha1().hexdigest()
    #
    #random_data = os.urandom(64)  # Generate 64 bytes of random data
    #job_id = hashlib.sha1(random_data).hexdigest()
    job_id = job['job_id']
    #
    # Delete job from tbl_job_queue
    #log_positive(f"DEBUG 004")
    cursor.execute(
        "DELETE FROM tbl_job_queue WHERE job_id = %s", 
        (job['job_id'],)
    )
    #log_positive(f"DEBUG 005")
    connection.commit()
    #log_positive(f"DEBUG 006")
    log_positive(f"Deleted job {job['job_id']} from queue")
    # Insert job into tbl_jobs
    job_insert_query = """
        INSERT INTO tbl_jobs 
        (job_id, job_type, job_category, geoname_id, job_target, job_status, job_owner, job_percent_complete, job_created_date, job_start_date, job_end_date, job_date_last_updated) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    #log_positive(f"DEBUG 007")
    job_insert_values = (job_id, job['job_type'], job['job_category'], job['geoname_id'], job['job_target'], 'New', 'job_owner', 0, job['job_created_date'], get_current_utc_time(), None, get_current_utc_time())
    #print(job_insert_values)
    #log_positive(f"DEBUG 009")
    cursor.execute(job_insert_query, job_insert_values)
    # Update job status
    #log_positive(f"DEBUG 010")
    job_status_insert_query = "INSERT INTO tbl_job_status (job_id, job_update_status, job_date_last_updated) VALUES (%s, %s, %s)"
    #log_positive(f"DEBUG 011")
    job_status_insert_values = (job_id, f"Job Created: {job_id}", get_current_utc_time())
    #log_positive(f"DEBUG 012")
    cursor.execute(job_status_insert_query, job_status_insert_values)
    #log_positive(f"DEBUG 013")
    connection.commit()
    #log_positive(f"DEBUG 014")
    # Grab the binary path, switches, and job parser
    cursor.execute("SELECT job_type_name, job_binary_path, job_switches, job_parser FROM tbl_job_type WHERE job_type_name = %s", (job['job_type'],))
    #log_positive(f"DEBUG 015")
    job_type = cursor.fetchone()
    # If there is no job_type then stop
    if not job_type:
        log_error("Job type not found")
        exit(1)
    # Check if the job binary path exists
    # If not try to correct it
    job_binary_path = job_type['job_binary_path']
    if not shutil.which(job_binary_path):
        job_binary_path = shutil.which(job['job_category'])
        if not job_binary_path:
            log_error(f"Job binary path not found for {job['job_category']}")
            exit(1)
    # Get the output file path
    # If it can't find it then stop
    cursor.execute("SELECT outputfile_name, outputfile_path FROM tbl_outputfile_path WHERE outputfile_name = %s", (job['job_category'],))
    outputfile = cursor.fetchone()
    if not outputfile:
        log_error("Output file path not found")
        exit(1)
    #log_positive(f"DEBUG 016")
    # Create the full output file path 
    outputfile_path_full = f"{outputfile['outputfile_path'].rstrip('/')}/{job_id}"
    # Modify the switchers that need to be ran with the target and the full outputfile path
    job_switches = job_type['job_switches'].replace("{target}", job['job_target']).replace("{outputfile}", outputfile_path_full)
    # Update the job status
    cursor.execute(job_status_insert_query, (job_id, f"Starting {job['job_category']} job: {job['job_target']}", get_current_utc_time()))
    cursor.execute("UPDATE tbl_jobs SET job_status = %s, job_percent_complete = %s, job_date_last_updated = %s WHERE job_id = %s", ('In Progress', 10, get_current_utc_time(), job_id))
    connection.commit()
    # Try to execute the job
    # If it fails then stop
    #log_positive(f"DEBUG 017")
    try:
        subprocess.run(f"{job_binary_path} {job_switches}", check=True, shell=True)
        cursor.execute(job_status_insert_query, (job_id, f"Completed {job['job_category']} job: {job['job_target']}", get_current_utc_time()))
        cursor.execute("UPDATE tbl_jobs SET job_percent_complete = %s, job_date_last_updated = %s WHERE job_id = %s", (75, get_current_utc_time(), job_id))
        connection.commit()
    except subprocess.CalledProcessError:
        log_error(f"Failed to run job: {job['job_target']}")
        exit(1)
    # Update the job status
    cursor.execute(job_status_insert_query, (job_id, f"Parsing {job['job_category']} parse job: {job['job_target']}", get_current_utc_time()))
    connection.commit()
    # Figure out where python3 is
    try:
        job_python_path = shutil.which('python3')
        log_positive(f"Job python path found: {job_python_path}")
    except:
        log_error(f"Job python path not found for {job['job_category']}")
        exit(1)
    # Try to run the parser to ingest into mysql
    try:
        subprocess.run(f"{job_python_path} {job_type['job_parser']} --inputfile {outputfile_path_full}.xml --jobid {job_id}", check=True, shell=True)
        cursor.execute(job_status_insert_query, (job_id, f"Completed {job['job_category']} parse job: {job['job_target']}", get_current_utc_time()))
        cursor.execute("UPDATE tbl_jobs SET job_percent_complete = %s, job_end_date = %s, job_date_last_updated = %s WHERE job_id = %s", (100, get_current_utc_time(), get_current_utc_time(), job_id))
        connection.commit()
    except subprocess.CalledProcessError:
        log_error(f"Failed to parse job output: {job['job_target']}")
        exit(1)
    # Set some variables
    scan_type = f"scans_{job['job_category']}"
    last_scan_datetime = f"last_scan_{job['job_category']}"
    #Get Current total_scans
    update_query = """
        Select total_scans FROM tbl_city_locations_en
        WHERE geoname_id = %s
    """
    cursor.execute(update_query, (job['geoname_id']))
    total_scans = cursor.fetchone()
    new_total_scans = total_scans[0] + 1
    log_positive(f"New updated scan total: {new_total_scans}")
    #
    update_query = f"UPDATE tbl_city_blocks_ipv4 SET {scan_type} = {new_total_scans}, {last_scan_datetime} = %s WHERE geoname_id = %s"
    cursor.execute(update_query, (get_current_utc_time(), job['geoname_id']))
    #
    cursor.execute(job_status_insert_query, (job_id, f"Updated tbl_city_blocks_ipv4 geoname_id: {job['geoname_id']}", get_current_utc_time()))
    connection.commit()
    #
    log_positive(f"Job {job_id} completed successfully")
except mysql.connector.Error as err:
    log_error(f"MySQL error: {err}")
except Exception as e:
    log_error(f"Unexpected error: {e}")
finally:
    cursor.close()
    connection.close()
