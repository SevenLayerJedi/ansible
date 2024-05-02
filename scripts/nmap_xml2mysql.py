#!/usr/bin/env python
import xml.etree.ElementTree as etree
import os
import csv
import argparse
from collections import Counter
from time import sleep
import mysql.connector
from mysql.connector import Error
import xml.etree.ElementTree as ET
import datetime
import pprint
import uuid
import hashlib


def generate_random_md5():
    random_uuid = uuid.uuid4()
    uuid_string = str(random_uuid)
    hash_object = hashlib.md5()
    hash_object.update(uuid_string.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


db_config = {
    'host': '10.200.1.91',
    'user': 'admin',
    'password': 'admin',
    'database': 'bbt'
}


def convert_unix_to_sql_datetime(unix_timestamp):
  timestamp = int(unix_timestamp)
  utc_datetime = datetime.datetime.utcfromtimestamp(timestamp)
  formatted_datetime = utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
  return formatted_datetime


def ingestion_time():
  current_utc_datetime = datetime.datetime.utcnow()
  formatted_datetime = current_utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
  return formatted_datetime


def get_host_data(root):
    host_data = []
    hosts = root.findall('host')
    for host in hosts:
        addr_info = []
        # Ignore hosts that are not 'up'
        if not host.findall('status')[0].attrib['state'] == 'up':
            continue
        # Get IP address and host info. If no hostname, then ''
        ip_address = host.findall('address')[0].attrib['addr']
        host_name_element = host.findall('hostnames')
        try:
            host_name = host_name_element[0].findall('hostname')[0].attrib['name']
        except IndexError:
            host_name = ''
        # Get the OS information if available, else ''
        try:
            os_element = host.findall('os')
            os_name = os_element[0].findall('osmatch')[0].attrib['name']
        except IndexError:
            os_name = ''
        # Grab Starttime and Endtime
        try:
            starttime = host.get('starttime')
            if starttime:
                try:
                    starttime = convert_unix_to_sql_datetime(starttime)
                    #print(" [+] Start Time: {0}".format(starttime))
                except:
                    print(" [-] Error convertingstarttime: {0}".format(starttime))
        except (IndexError, KeyError):
            starttime = ''
        try:
            endtime = host.get('endtime')
            if endtime:
                try:
                    endtime = convert_unix_to_sql_datetime(endtime)
                    #print(" [+] End Time: {0}".format(endtime))
                except:
                    print(" [-] Error converting endtime: {0}".format(endtime)) 
        except (IndexError, KeyError):
            endtime = ''
        #
        # Get information on ports and services
        try:
            port_element = host.findall('ports')
            ports = port_element[0].findall('port')
            for port in ports:
                port_data = []
                proto = port.attrib['protocol']
                port_id = port.attrib['portid']
                service = port.findall('service')[0].attrib['name']
                service_all = port.find('service')
                state_element = port.find('state')
                # Grab state Info
                if state_element is not None:
                    try:
                        state = state_element.get('state')
                    except (IndexError, KeyError):
                        state = ''
                    try:
                        state_reason = state_element.get('reason')
                    except (IndexError, KeyError):
                        state_reason = ''
                    try:
                        state_reason_ttl = state_element.get('reason_ttl')
                    except (IndexError, KeyError):
                        state_reason_ttl = ''
                # Grab Service Info
                if service is not None:
                    try:
                        service_version = service_all.get('version', '')
                    except (IndexError, KeyError):
                        service_version = ''
                    try:
                        service_extrainfo = service_all.get('extrainfo', '')
                    except (IndexError, KeyError):
                        service_extrainfo = ''
                    try:
                        service_cpes = ', '.join(cpe.text for cpe in service_all.findall('cpe'))
                    except (IndexError, KeyError):
                        service_cpes = ''
                    try:
                        service_method = service_all.get('method', '')
                    except (IndexError, KeyError):
                        service_method = ''
                    try:
                        service_ostype = service_all.get('ostype', '')
                    except (IndexError, KeyError):
                        service_ostype = ''
                    try:
                        service_conf = service_all.get('conf', '')
                    except (IndexError, KeyError):
                        service_conf = ''
                try:
                    product = port.findall('service')[0].attrib['product']
                except (IndexError, KeyError):
                    product = ''
                try:
                    tunnel = port.findall('service')[0].attrib['tunnel']
                except (IndexError, KeyError):
                    tunnel = ''     
                try:
                    servicefp = port.findall('service')[0].attrib['servicefp']
                except (IndexError, KeyError):
                    servicefp = ''
                try:
                    script_id = port.findall('script')[0].attrib['id']
                except (IndexError, KeyError):
                    script_id = ''
                try:
                    script_output = port.findall('script')[0].attrib['output']
                except (IndexError, KeyError):
                    script_output = ''
                #
                #  NMAP_NAME            MYSQL_NAME              VARIABLE
                #
                # Main Section
                ## n/a                  ingestion_datetime      ingestion_time()
                ## n/a                  start_time              starttime
                ## n/a                  end_time                endtime
                ## job_id               job_id                  jobID
                ## hostname             hostname               host_name
                ## addr                 ip_addr                 ip_address
                ## port_id              port_id                 port_id
                ## protocol             protocol                proto
                ## 
                #
                # Service Section
                ## conf                 service_conf            service_conf
                ## method               service_method          service_method
                ## name                 service_name            service
                ## ostype               service_os_type         os_name
                ## product              service_product         product
                ## extrainfo            service_extrainfo       service_extrainfo
                ## tunnel               service_tunnel          tunnel
                ## version              service_version         service_version
                ## cpe                  service_cpes            service_cpes
                ## servicefp            service_fingerprint     servicefp
                # 
                # State Section
                ## state                state                   state
                ## reason               state_reason            state_reason
                ## reason_ttl           state_reason_ttl        state_reason_ttl
                #
                # Script Section
                ## id                   script_id               script_id
                ## output               script_output           script_output
                #
                # Create a list of the port data
                port_data.extend((ingestion_time(), starttime, endtime, jobID, host_name, ip_address, port_id, proto,
                                service_conf, service_method, service, os_name, product, service_extrainfo, 
                                tunnel, service_version, service_cpes, servicefp,
                                state, state_reason, state_reason_ttl,
                                script_id, script_output))
                # Add the port data to the host data
                host_data.append(port_data)
        # If no port information, just create a list of host information
        except IndexError:
            pass
    return host_data


def parse_xml(filename):
    try:
        tree = etree.parse(filename)
    except Exception as error:
        print("[-] A an error occurred. The XML may not be well formed. "
              "Please review the error and try again: {}".format(error))
        exit()
    root = tree.getroot()
    scan_data = get_host_data(root)
    return scan_data


def parse_to_mysql(data, db_config):
    """Given a list of data, inserts the items into a MySQL database."""
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # port_data.extend((ingestion_time(), starttime, endtime, jobID, host_name, ip_address, port_id, proto,
            #     service_conf, service_method, service, os_name, product, service_extrainfo, 
            #     tunnel, service_version, service_cpes, servicefp,
            #     state, state_reason, state_reason_ttl,
            #     script_id, script_output))
            #
            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_nmap (
                    ingestion_datetime DATETIME,
                    start_time DATETIME,
                    end_time DATETIME,
                    job_id VARCHAR(255),
                    hostname VARCHAR(255),
                    ip_addr VARCHAR(255),
                    port_id INT,
                    protocol VARCHAR(255),
                    service_conf VARCHAR(255),
                    service_method VARCHAR(255),
                    service_name VARCHAR(255),
                    os_type VARCHAR(255),
                    service_product VARCHAR(255),
                    service_extrainfo VARCHAR(255),
                    service_tunnel VARCHAR(255),
                    service_version VARCHAR(255),
                    service_cpes VARCHAR(255),
                    service_fingerprint TEXT,
                    state VARCHAR(255),
                    state_reason VARCHAR(255),
                    state_ttl VARCHAR(255),
                    script_id VARCHAR(255),
                    script_output TEXT
                );
            ''')
            connection.commit()
            #
            # Insert data into the table
            insert_query = '''
                INSERT INTO tbl_nmap (
                    ingestion_datetime, start_time, end_time, job_id, hostname,
                    ip_addr, port_id, protocol, service_conf, service_method,
                    service_name, os_type, service_product, service_extrainfo,
                    service_tunnel, service_version, service_cpes, service_fingerprint,
                    state, state_reason, state_ttl, script_id, script_output
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''
            cursor.executemany(insert_query, data)
            connection.commit()
            print('\n[+] Data inserted successfully!\n')
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("[+] MySQL connection is closed")


def parse_to_mysql_test(data):
    """Test Data Output"""
    #pprint.pp(data)
    #print(type(data))
    print(data)


def parse_to_csv(data):
    """Given a list of data, adds the items to (or creates) a CSV file."""
    if not os.path.isfile(csv_name):
        csv_file = open(csv_name, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        top_row = [
            'IP', 'Host', 'OS', 'Proto', 'Port',
            'Service', 'Product', 'Service FP',
            'NSE Script ID', 'NSE Script Output', 'Notes'
        ]
        csv_writer.writerow(top_row)
        print('\n[+] The file {} does not exist. New file created!\n'.format(
                csv_name))
    else:
        try:
            csv_file = open(csv_name, 'a', newline='')
        except PermissionError as e:
            print("\n[-] Permission denied to open the file {}. "
                  "Check if the file is open and try again.\n".format(csv_name))
            print("Print data to the terminal:\n")
            if args.debug:
                print(e)
            for item in data:
                print(' '.join(item))
            exit()
        csv_writer = csv.writer(csv_file)
        print('\n[+] {} exists. Appending to file!\n'.format(csv_name))
    for item in data:
        csv_writer.writerow(item)
    csv_file.close()


def get_uri(ip, service, port):
    http_port_list = ['80', '280', '81', '591', '593', '2080', '2480', '3080', 
                      '4080', '4567', '5080', '5104', '5800', '6080',
                      '7001', '7080', '7777', '8000', '8008', '8042', '8080',
                      '8081', '8082', '8088', '8180', '8222', '8280', '8281',
                      '8530', '8887', '9000', '9080', '9090', '16080']                    
    https_port_list = ['832', '981', '1311', '7002', '7021', '7023', '7025',
                       '7777', '8333', '8531', '8888']
    ftp_port_list = ['20', '21']
    sftp_port_list = ['22', '2222']
    ftps_port_list = ['990']
    smb_port_list = ['139', '445']
    smtp_port_list = ['25', '587']
    smtps_port_list = ['465']
    telnet_port_list = ['23', '2323']
    irc_port_list = ['194']
    ircs_port_list = ['6697']
    rtsp_port_list = ['554', '8554']
    ldap_port_list = ['389']
    ldaps_port_list = ['636']
    ssh_port_list = ['22']


    if port.endswith('43') and port != "143" or port in https_port_list:
        uri = "https://{}:{}".format(ip, port)
    elif port in http_port_list:
        uri = "http://{}:{}".format(ip, port)
    else:
        uri = ''
    return uri    


def print_filtered_port(data, filtered_port):
    """Examines the port index from data and see if it matches the 
    filtered_port. If it matches, print the IP address.
    """
    for item in data:
        try:
            port = item[4]
        except IndexError as e:
            if args.debug:
                print(e)
            continue
        if port == filtered_port:
            print(item[0])


def print_data(data):
    for item in data:
        print(' '.join(item))


def main():
    for filename in args.filename:
        # Checks the file path
        if not os.path.exists(filename):
            parser.print_help()
            print("\n[-] The file {} cannot be found or you do not have "
                  "permission to open the file.".format(filename))
            continue
        data = parse_xml(filename)
        if not data:
            print("[*] Zero hosts identitified as 'Up' or with 'open' ports. "
                  "Use the -u option to display ports that are 'open|filtered'. "
                  "Exiting.")
            exit()
        if args.csv:
            parse_to_csv(data)
        if args.mysql:
            parse_to_mysql(data, db_config)
            #parse_to_mysql_test(data)
        print(" [+] jobID: {0}".format(jobID))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-csv", "--csv",
                        nargs='?', const='scan.csv',
                        help="Specify the name of a csv file to write to. "
                             "If the file already exists it will be appended")
    parser.add_argument("-mysql", "--mysql",
                        nargs='?', const='scan.csv',
                        help="Import data to mysql. ")
    parser.add_argument("-f", "--filename",
                        nargs='*',
                        help="Specify a file containing the output of an nmap "
                             "scan in xml format.")
    parser.add_argument("-j", "--jobid",
                        nargs='*',
                        help="Specify the jobID "
                             "this is a random md5 hash.")
    args = parser.parse_args()
    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify an input file to parse. "
              "    python3 nmap_xml2mysql.py -f <nmap_scan.xml> -j <jobID>\n")
        exit()
    if args.csv:
        csv_name = args.csv
    #csv_name = /opt/nmap/test/
    #filename = /opt/nmap/test/162.244.69.0_24.xml
    if args.jobid:
        jobID = args.jobid
    else:
        jobID = generate_random_md5()
    main()
