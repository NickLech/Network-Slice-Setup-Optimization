#!/usr/bin/env python3

from comnetsemu.net import Containernet
from comnetsemu.node import DockerHost
from mininet.node import Controller
from mininet.cli import CLI


def main():
    # Create Containernet
    net = Containernet(controller=Controller)
    net.addController("c0")

    # Switches (Multi-hop topology)
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    s3 = net.addSwitch("s3")

    # Hosts (clients)
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")

    # Docker servers (service instances)
    serverA = net.addDocker(
        "serverA",
        ip="10.0.0.10/24",
        dimage="ubuntu:latest",
        dcmd="/bin/bash"
    )

    serverB = net.addDocker(
        "serverB",
        ip="10.0.0.11/24",
        dimage="ubuntu:latest",
        dcmd="/bin/bash"
    )

    # Links (you can assign custom bandwidth/delay)
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(s1, s2)
    net.addLink(s2, s3)

    net.addLink(s3, serverA)
    net.addLink(s3, serverB)

    # Start network
    net.start()

    print("*** Topology ready. Start CLI.")
    CLI(net)

    net.stop()


if __name__ == "__main__":
    main()
