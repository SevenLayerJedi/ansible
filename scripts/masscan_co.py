import pymysql
import subprocess
import os
import time

# Database configuration
db_config = {
    'host': '10.200.1.91',
    'user': 'admin',
    'password': 'admin',
    'database': 'bbt'
}

def fetch_networks():
    connection = pymysql.connect(host=db_config['host'],
                                 user=db_config['user'],
                                 password=db_config['password'],
                                 database=db_config['database'])
    networks = []
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT network
            FROM `tbl_city_blocks_ipv4`
            WHERE geoname_id IN (
                SELECT geoname_id
                FROM `tbl_city_locations_en`
                WHERE subdivision_1_iso_code = 'CO'
            );
            """
            cursor.execute(query)
            results = cursor.fetchall()
            networks = [row[0] for row in results]
    except Exception as e:
        print(f"An error occurred while fetching networks: {e}")
    finally:
        connection.close()
    return networks

def create_directory(path):
    try:
        # Use exist_ok=True to avoid an error if the directory already exists
        os.makedirs(path, exist_ok=True)
        #print(f" [+] Directory '{path}' was created successfully.")
        print(Fore.GREEN + f"  [+] Directory '{path}' was created successfully.")
    except OSError as error:
        #print(f" [-] Error creating directory {path}: {error}")
        print(Fore.RED + f"  [-] Error creating directory {path}: {error}")


    cursor.execute("SELECT job_binary_path, job_switches FROM tbl_job_type WHERE job_type_name = %s", (job_type,))
    job_binary_path, job_switches = cursor.fetchone()
    #
    # Check if the nmap binary exists at the specified path, or find it in the system PATH
    if not shutil.which(job_binary_path):
        job_binary_path = shutil.which("nmap")
                #


def run_masscan(networks):
    total_networks = len(networks)
    start_time = time.time()
    # Create the DIrectory
    job_category = 'masscan'
    cursor.execute("SELECT outputfile_path FROM tbl_outputfile_path WHERE outputfile_name = %s", (job_category,))
    output_file_path = cursor.fetchone()[0]
    create_directory(output_file_path)
    #
    for index, network in enumerate(networks, 1):
        network_start_time = time.time()
        filename = network.replace('/', '_')  # Replace forward slashes
        output_path = f"/opt/bbt/masscan/{filename}.xml"
        command = [
            "sudo", "masscan", "--rate=1000", "--banners", "--open-only",
            "--retries=3", "--top-ports", "3328", "-oX", output_path, network
        ]
        print(f"Running masscan on {network} ({index}/{total_networks})")
        try:
            subprocess.run(command, check=True)
            print(f"Masscan completed for {network}, output saved to {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error running masscan for {network}: {e}")
        elapsed_time = time.time() - network_start_time
        remaining_networks = total_networks - index
        if remaining_networks > 0:
            estimated_time = (elapsed_time * remaining_networks) / 60
            print(f"Completed {index}/{total_networks} networks ({(index/total_networks)*100:.2f}%). Estimated time to finish: {estimated_time:.2f} minutes.")
        else:
            total_elapsed_time = (time.time() - start_time) / 60
            print(f"All networks scanned. Total time taken: {total_elapsed_time:.2f} minutes.")

# Main function
def main():
    networks = fetch_networks()
    if networks:
        run_masscan(networks)
    else:
        print("No networks to scan.")

if __name__ == "__main__":
    main()
