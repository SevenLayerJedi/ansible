# Create Private Internet Access secret Creds
kubectl create secret generic pia-credentials --from-env-file=private/pia-credentials.env