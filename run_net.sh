#!/bin/bash

# Run topology
if ! command -v python3.9 >/dev/null 2>&1
then
    sudo python3 ./topology.py
else
    sudo python3.9 ./topology.py
fi

# Cleanup
echo "Cleaning up..."
sudo mn -c
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# Remove old DNS records
rm -rf config/dns_config/zones/*

echo "Cleanup complete"