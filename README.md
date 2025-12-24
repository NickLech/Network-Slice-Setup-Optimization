## NB: All steps to be done in the Mininet VM

# Setup
Pull DNS container image from Docker:
```
docker pull technitium/dns-server
```

Build image:
```
cd dns_docker
docker build -t dns-mn .
cd ..
```

# Run
Make sure that port 53 is free for binding:
```
sudo sh dns_docker/stop_systemd_resolve.sh
```

Backup /etc/resolv.conf if necessary, because the script will overwrite it.
    
In a terminal:
```
ryu run controller/controller_main.py
```

In a second terminal:
```
sudo python3 topology.py
```

# Check mininet-host connectivity and services
net tools:
```
h13 ifconfig
```

services:
```
h17 curl -I http://10.0.0.13:80
h8 wget http://10.0.0.3:4380/video.dat
```

# Every time you restart make sure to clean all the previous stroz
```
sudo mn -c
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
```