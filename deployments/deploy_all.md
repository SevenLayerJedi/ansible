cd /opt/ansible && git pull

sudo kubectl apply -f /opt/ansible/deployments/deploy_gluetun.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_mysql.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_phpmyadmin.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_webserver.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_worker.yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_job_producer.yaml

sudo kubectl create secret generic pia-creds --from-env-file=/opt/pia/pia_creds.env


# Get all Pods
sudo kubectl get pods

# Describe Pod
sudo kubectl describe mysql-5879c7ccf7-xg7ll

# Get Logs
sudo kubectl logs mysql-5879c7ccf7-xg7ll

# Execute Shell
sudo kubectl exec -it mysql-5bb8b89cbf-cqlpw -- /bin/sh
sudo kubectl exec -it gluetun-6b964c6d6-xjghj -- /bin/sh
sudo kubectl exec -it phpmyadmin-6d56c5bd4-m7smc -- /bin/sh

# Test mysql container
docker run -it --name mysql-debug bugbountytools/mysql-cron-ubuntu /bin/bash


# Redploy
sudo kubectl rollout restart deployment gluetun


# List all pods
sudo kubectl get pods -o wide

# List all deployments
sudo kubectl get deployments

# Delete pod
sudo kubectl delete pod <mysql-pod-name>

# Delete Deployment
sudo kubectl delete deployment gluetun
sudo kubectl delete deployment phpmyadmin
sudo kubectl delete deployment mysql

# Deploy deployment yaml
sudo kubectl apply -f /opt/ansible/deployments/deploy_all.yaml

# Create Namespace
sudo kubectl create namespace bugbounty

# List pods for namespace
sudo kubectl get pods -n bugbounty -o wide

#
kubectl describe pod app-with-gluetun -n bugbounty

# Create creds for namespace
sudo kubectl create secret generic pia-creds --from-env-file=/opt/pia/pia_creds.env -n bugbounty

# Describe the new pod
sudo kubectl describe pod app-with-gluetun -n bugbounty











