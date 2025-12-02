from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub

class SimpleController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # gli switch sono i datapath
    # ogni switch è identificato da un ID univoco (datapath.id)

    # inizializzazione del controller
    def __init__(self, *args, **kwargs):
        super(SimpleController, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    # gestione dei cambiamenti di stato dei datapath
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if datapath.id not in self.datapaths:
            self.datapaths[datapath.id] = datapath

    # periodicamente richiede statistiche ai datapath
    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)

    # richiede statistiche delle porte di uno switch mediante API OpenFlow
    def _request_stats(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    # gestione della risposta delle statistiche delle porte
    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        print("\n=== Port Statistics for Switch DPID: {} ===".format(ev.msg.datapath.id))
        print("{:<8} {:<10} {:<10} {:<10} {:<10}".format("Port", "RX-pkts", "TX-pkts", "RX-bytes", "TX-bytes"))
        print("-" * 50)
        for stat in ev.msg.body:
            print("{:<8} {:<10} {:<10} {:<10} {:<10}".format(
                stat.port_no, stat.rx_packets, stat.tx_packets, stat.rx_bytes, stat.tx_bytes))
        print("=" * 50)


# TODO:
# - controllare se gli spine switch danno effettivamente le statistiche
# - stimare bandwidth e delay basandosi su queste statistiche
#   - per la stima della bandwidth si può usare la formula:
#     bandwidth = (tx_bytes_now - tx_bytes_prev) * 8 / time_interval(s)     [o con rx_bytes, o una media delle due]
#   - per la stima del delay si deve fare con ping su mininet
# - Nel caso volessimo passare a OFP 1.5
# - con ryu.ofproto.ofproto_v1_5_parser.OFPPortMod si può mettere una porta down/up
# - ryu.ofproto.ofproto_v1_5_parser.OFPMeterMod modifica le metriche di una porta di uno switch
# - ryu.ofproto.ofproto_v1_5_parser.OFPPortStatus lo switch lo invia quando una porta cambia stato (up/down), sembra che ci sia anche info su bandwidth (teorica)