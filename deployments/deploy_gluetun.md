# Create Private Internet Access secret Creds
sudo kubectl create secret generic pia-credentials --from-env-file=/opt/ansible/config/pia_creds.env

