UPDATE `tbl_job_type` SET
job_parser = '/opt/ansible/parsers/nmap_xml2mysql.py'
WHERE job_type_name = 'nmap_full_tcp'
