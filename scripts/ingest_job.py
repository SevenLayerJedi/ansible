import pymysql
import subprocess
import shutil
import socket
from datetime import datetime
from colorama import Fore, init
import os


# Initialize colorama for colored console output
init(autoreset=True)

# Database configuration
db_config = {
    'host': '10.200.1.91',
    'user': 'admin',
    'password': 'admin',
    'database': 'bbt'
}

def update_job_table(jobID, jobStatus, percentComplete, endDate):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Update job status in 'tbl_jobs'
            current_utc = datetime.utcnow()
            update_query = """
                UPDATE tbl_jobs SET
                job_status = %s,
                job_percent_complete = %s,
                job_end_date = %s,
                job_date_last_updated = %s
                WHERE job_id = %s
            """
            cursor.execute(update_query, (jobStatus, percentComplete, endDate, current_utc, jobID))
            connection.commit()
            print("  [+] Job Table Updated")
    except Exception as e:
        print(f"  [-] Failed to update Job Table: {e}")
        connection.rollback()
    finally:
        connection.close()


def update_city_locations_table(jobID, geoNameID):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Update job status in 'tbl_jobs'
            current_utc = datetime.utcnow()
            #
            #Get Current total_scans
            update_query = """
                Select total_scans FROM tbl_city_locations_en
                WHERE geoname_id = %s
            """
            cursor.execute(update_query, (geoNameID))
            total_scans = cursor.fetchone()
            # Update Fields
            update_query = """
                UPDATE tbl_city_locations_en SET
                total_scans = %s,
                last_scanned_datetime = %s
            """
            cursor.execute(update_query, (total_scans + 1, current_utc))
            connection.commit()
            print("  [+] Job Table Updated")
            update_job_status(jobID, f"Updated tbl_city_locations_en Successfully")
    except Exception as e:
        print(f"  [-] Failed to update tbl_city_locations_en: {e}")
        update_job_status(jobID, f"Failed to update tbl_city_locations_en: {e}")
        connection.rollback()
    finally:
        connection.close()


def update_job_status(jobID, jobUpdateStatus):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Update job status in 'tbl_jobs'
            current_utc = datetime.utcnow()
            #
            # Insert new status in 'tbl_job_status'
            status_query = """
                INSERT INTO tbl_job_status (job_id, job_update_status, job_date_last_updated)
                VALUES (%s, %s, %s)
            """
            cursor.execute(status_query, (jobID, jobUpdateStatus, current_utc))
            connection.commit()
            print("  [+] Job status updated")
    except Exception as e:
        print(f"  [-] Failed to update job staatus: {e}")
        connection.rollback()
    finally:
        connection.close()


def create_directory(path):
    try:
        # Use exist_ok=True to avoid an error if the directory already exists
        os.makedirs(path, exist_ok=True)
        #print(f" [+] Directory '{path}' was created successfully.")
        print(Fore.GREEN + f"  [+] Directory '{path}' was created successfully.")
    except OSError as error:
        #print(f" [-] Error creating directory {path}: {error}")
        print(Fore.RED + f"  [-] Error creating directory {path}: {error}")


def main():
    try:
        # Connect to MySQL database
        connection = pymysql.connect(host=db_config['host'],
                                     user=db_config['user'],
                                     password=db_config['password'],
                                     database=db_config['database'])
        print(Fore.GREEN + "  [+] Connected to the database successfully")
        #
        with connection.cursor() as cursor:
            # Query the oldest job in the queue
            cursor.execute("""
                SELECT job_id, job_type, job_category, geoname_id, job_target, job_created_date
                FROM tbl_job_queue
                ORDER BY job_created_date
                LIMIT 1
            """)
            job = cursor.fetchone()
            if job:
                print(Fore.GREEN + "  [+] Setting variables from query")
                job_id, job_type, job_category, geoname_id, job_target, job_created_date = job
                #
                # Get the hostname of the computer running this script
                print(Fore.GREEN + "  [+] Getting Hostname")
                hostname = socket.gethostname()
                #
                # Insert job into tbl_jobs
                current_utc = datetime.utcnow()
                cursor.execute("""
                    INSERT INTO tbl_jobs (job_id, job_type, job_category, geoname_id, job_target, job_status, job_owner,
                                          job_percent_complete, job_created_date, job_start_date,
                                          job_end_date, job_date_last_updated)
                    VALUES (%s, %s, %s, %s, %s, 'New', %s, 0, %s, %s, NULL, %s)
                """, (job_id, job_type, job_category, geoname_id, job_target, hostname, job_created_date, current_utc, current_utc))
                print(Fore.GREEN + "  [+] Job inserted into tbl_jobs")
                update_job_status(job_id, 'NMAP Job Created and Added to tbl_jobs')
                #
                # Delete the job from tbl_job_queue
                cursor.execute("DELETE FROM tbl_job_queue WHERE job_id = %s", (job_id,))
                print(Fore.GREEN + "  [+] Job removed from tbl_job_queue")
                update_job_status(job_id, 'NMAP Job Removed from tbl_job_queue')
                #
                # Commit changes
                connection.commit()
                #
                # Prepare to execute the command
                cursor.execute("SELECT outputfile_path FROM tbl_outputfile_path WHERE outputfile_name = %s", (job_category,))
                output_file_path = cursor.fetchone()[0]
                #
                create_directory(output_file_path)
                #
                cursor.execute("SELECT job_binary_path, job_switches FROM tbl_job_type WHERE job_type_name = %s", (job_type,))
                job_binary_path, job_switches = cursor.fetchone()
                #
                # Check if the nmap binary exists at the specified path, or find it in the system PATH
                if not shutil.which(job_binary_path):
                    job_binary_path = shutil.which("nmap")
                #
                # Execute the nmap command
                output_file = f"{output_file_path}/{job_id}"
                target = job_target
                command = job_switches.replace("{outputfile}", output_file).replace("{target}", target)
                full_command = f"{job_binary_path} {command}"
                update_job_status(job_id, 'NMAP Executing Command: {0}'.format(full_command))
                update_job_table(job_id, 'In Progres', 10, None)
                if subprocess.run(full_command, shell=True, check=True):
                    print(Fore.GREEN + "  [+] Command executed successfully")
                    update_job_status(job_id, 'NMAP Scan Completed')
                    update_job_table(job_id, 'Completed', 100, datetime.utcnow())
                    update_city_locations_table(job_id, geoname_id)
            else:
                print(Fore.YELLOW + "  [-] No jobs found in the queue")
    except Exception as e:
        print(Fore.RED + f"  [-] An error occurred: {e}")
        update_job_status('ERROR', f"  [-] An error occurred: {e}")
        connection.rollback()
    finally:
        connection.close()
        print(Fore.GREEN + "  [+] Database connection closed")

if __name__ == "__main__":
    main()
