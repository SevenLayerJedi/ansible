network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      dhcp6: false
      addresses:
      - 10.200.1.90/16
      routes:
      - to: default
        via: 10.200.0.1
      nameservers:
       addresses: [1.1.1.1,8.8.8.8]