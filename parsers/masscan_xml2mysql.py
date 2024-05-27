import argparse
import xml.etree.ElementTree as ET
import mysql.connector
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

def create_table_if_not_exists(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tbl_masscan (
        ingestion_datetime DATETIME,
        start_time DATETIME,
        end_time DATETIME,
        job_id VARCHAR(256),
        ip_addr VARCHAR(256),
        ip_addr_type VARCHAR(256),
        protocol VARCHAR(256),
        port_id VARCHAR(256),
        state VARCHAR(256),
        state_reason VARCHAR(256),
        state_ttl VARCHAR(256),
        service_name VARCHAR(256),
        banner VARCHAR(256)
    )
    """
    cursor.execute(create_table_query)

def parse_and_ingest(xml_file, job_id, cursor):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    #
    for host in root.findall('host'):
        start_time = get_current_utc_time()
        addr = host.find('address').attrib['addr']
        addrtype = host.find('address').attrib['addrtype']
        #
        ports = host.find('ports')
        for port in ports.findall('port'):
            protocol = port.attrib['protocol']
            portid = port.attrib['portid']
            state_elem = port.find('state')
            state = state_elem.attrib['state']
            reason = state_elem.attrib['reason']
            reason_ttl = state_elem.attrib['reason_ttl']
            service = port.find('service')
            if service is not None:
                name = service.attrib.get('name', '')
                banner = service.attrib.get('banner', '')
            else:
                name = ''
                banner = ''
            end_time = get_current_utc_time()
            ingestion_datetime = get_current_utc_time()
            insert_query = """
            INSERT INTO tbl_masscan (
                ingestion_datetime, start_time, end_time, job_id, ip_addr, ip_addr_type, 
                protocol, port_id, state, state_reason, state_ttl, service_name, banner
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                ingestion_datetime, start_time, end_time, job_id, addr, addrtype, protocol, 
                portid, state, reason, reason_ttl, name, banner
            ))

def main():
    parser = argparse.ArgumentParser(description="Parse masscan XML and ingest data into MySQL")
    parser.add_argument('--inputfile', required=True, help='Path to the masscan XML file')
    parser.add_argument('--jobid', required=True, help='Job ID')
    args = parser.parse_args()
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        create_table_if_not_exists(cursor)
        parse_and_ingest(args.inputfile, args.jobid, cursor)
        connection.commit()
        log_positive("Data ingested successfully")
    except mysql.connector.Error as err:
        log_error(f"MySQL error: {err}")
    except Exception as e:
        log_error(f"Unexpected error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main()
