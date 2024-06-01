kubectl apply -f /opt/ansible/deployments/deploy_gluetun.yaml
kubectl apply -f /opt/ansible/deployments/deploy_mysql.yaml
kubectl apply -f /opt/ansible/deployments/deploy_phpmyadmin.yaml
kubectl apply -f /opt/ansible/deployments/deploy_webserver.yaml
kubectl apply -f /opt/ansible/deployments/deploy_worker.yaml
kubectl apply -f /opt/ansible/deployments/deploy_job_producer.yaml

kubectl create secret generic pia-creds --from-env-file=/opt/pia/pia_creds.env




