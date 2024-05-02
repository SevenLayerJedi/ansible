####
apt-get install  samba-common smbclient samba-common-bin smbclient  cifs-utils

#####
sudo mkdir /mnt/picluster
sudo mount -t cifs //10.200.1.242/picluster /mnt/picluster -o user=admin,pass=notmypassword

