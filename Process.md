

Each node Crontab every 60 seconds
    Check if number of running containers is less than x
    Check if overal CPU/MEM is below x
        THen ask mariadb if there are any new jobs
        If there is a job then 
            make sure docker volume exists
            create UID
            create targetname
            get date in unix format
            update db with in progress status



Check target list for anything that hasn't been scanned in x minutes
    create jobs
Check bugbounty sites for new targets
    update db with new targets




tbl_targets
    target_name         google
    target_uid          Dik98diekIK8762A
    target_scope        bugcrowd/hackerone
    target_inscope      google.com/chat.google.com
    target_addedtime    current time
    target_lastupdated  current time


tbl_jobs
    job_name            nmap
    job_scope           bugcrowd/hackerone
    job_switches        -sC -sV -oX /opt/output/
    job_target          google.com
    job_status          available/running/finished
    job_starttime       
    job_finishtime
    node_assigned       pinode02


folder structure
opt
  jobs
    %targetname%
      nmap
      masscan
      nikto
      crawler
