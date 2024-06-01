network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      dhcp6: false
      addresses:
      - 10.200.2.90/16
      routes:
      - to: default
        via: 10.200.0.1
      nameservers:
       addresses: [1.1.1.1,8.8.8.8]
  wifis:
    renderer: networkd
    wlan0:
      dhcp4: false
      dhcp6: false
      addresses: [10.200.1.90/16]
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
      access-points:
        Rosay All Day:
          password: 172c1e67c601849b0d4258bf3cec5e78e17e9fef9b2406fe4f01198b82492271
      routes:
        - to: default
          via: 10.200.0.1
