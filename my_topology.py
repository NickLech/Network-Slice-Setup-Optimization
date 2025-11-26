#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def complex_topology():
    net = Mininet(controller=Controller, link=TCLink)
    net.addController('c0')

    # Aggiunta switch
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Collegamenti tra switch (ring topology)
    net.addLink(s1, s2, bw=100, delay='5ms')
    net.addLink(s2, s3, bw=100, delay='5ms')
    net.addLink(s3, s1, bw=100, delay='5ms')

    # Aggiunta host e link
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')

    net.addLink(h1, s1, bw=50)
    net.addLink(h2, s1, bw=50)
    net.addLink(h3, s2, bw=50)
    net.addLink(h4, s2, bw=50)
    net.addLink(h5, s3, bw=50)
    net.addLink(h6, s3, bw=50)

    net.start()

    # Eventi simulati: funzione di esempio per disabilitare un link dopo 30s e aggiungere traffico
    def simulate_environment():
        import time
        time.sleep(30)
        print("Simulating link failure between s1 and s2")
        link = net.linksBetween(s1, s2)[0]
        net.configLinkStatus(s1.name, s2.name, 'down')
        # Puoi aggiungere traffico o migrazioni qui via script northbound

    # Lancia simulazione ambientale in parallelo
    import threading
    env_thread = threading.Thread(target=simulate_environment)
    env_thread.start()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    complex_topology()
