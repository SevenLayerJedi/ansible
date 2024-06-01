cd /opt/ansible && git pull


sudo kubectl apply -f /opt/ansible/deployments/deploy_mysql.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_phpmyadmin.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_webserver.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_worker.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_job_producer.yaml

sudo kubectl create secret generic pia-creds --from-env-file=/opt/pia/pia_creds.env




