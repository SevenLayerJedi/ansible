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
sudo kubectl exec -it gluetun-56d758897c-8dmg5 -- /bin/sh

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




