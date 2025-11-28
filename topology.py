#!/usr/bin/env python3

import random
import threading
import time

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel


def scalable_topology(K=3, H=2, T=20, auto_recover=True):
    """
    - 1 spine switch
    - K leaf switches
    - H host per leaf
    - Ogni T secondi cade un leaf
    """

    net = Mininet(controller=Controller, link=TCLink)
    net.addController('c0')

    # Spine switch
    spine = net.addSwitch('s1')

    # Leaf switches
    leaf_switches = []
    for i in range(K):
        leaf = net.addSwitch(f's{i+2}')
        leaf_switches.append(leaf)
        net.addLink(spine, leaf, bw=100, delay='5ms')

        # Aggiunta host per leaf
        for h in range(H):
            host = net.addHost(f'h{len(net.hosts) + 1}')
            net.addLink(host, leaf, bw=50)

    net.start()

    def environmental_events():
        while True:
            time.sleep(T)

            # Selezione leaf casuale
            leaf = random.choice(leaf_switches)
            print(f"\n*** EVENTO: disabilito link spine <-> {leaf.name}\n")

            net.configLinkStatus('s1', leaf.name, 'down')

            if auto_recover:
                time.sleep(T)
                print(f"\n*** RECOVERY: riattivo link spine <-> {leaf.name}\n")
                net.configLinkStatus('s1', leaf.name, 'up')

    # Avvia thread parallelo
    event_thread = threading.Thread(target=environmental_events, daemon=True)
    event_thread.start()

    # Avvia Mininet CLI
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    scalable_topology(K=3, H=2, T=15, auto_recover=True)
