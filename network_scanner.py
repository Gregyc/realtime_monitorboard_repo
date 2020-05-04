import scapy.all as scapy

DGBOARD_MAC_ADDR_KEY = "60:00"

def scan_ip (host_ip_addr):




    # 1. Create ARP request directed to broadcast MAC asking for the IP
    # Classless Inter-Domain Routing (CIDR) 
    # a.b.c.0/24 means the ip range is from a.b.c.0 - a.b.c.255 (submask=255.255.255.0)
    # a.b.0.0/24 means the ip range is from a.b.0.0 - a.b.255.255 (submask=255.255.0.0)
    target_ip = host_ip_addr+"/24"
    # IP Address for the destination
    # create ARP packet
    arp = scapy.ARP(pdst=target_ip)

    # 2. Set destination MAC to broadcast MAC
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # combine the ARP and broadcast packet, and it will automatically send to broadcast MAC
    packet = broadcast/arp

    result = scapy.srp(packet, timeout=15, verbose=0)[0]

    # a list of clients, we will fill this in the upcoming loop
    clients = []
    ips = []

    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        # only keep the digital board IP and MAC (assume MAC starts with "60:00")
        if received.hwsrc.startswith(DGBOARD_MAC_ADDR_KEY):
            clients.append({'ip': received.psrc, 'mac': received.hwsrc})
            ips.append(received.psrc)
    return ips


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip





if __name__ == "__main__":
    dgboard_ip_list = []
    dgboard_ip_list = scan_ip('192.168.2.1')

    if not dgboard_ip_list :
        raise RuntimeError('Do not detect any board, check connection!!')
    else:    
        # print clients
        print("Available devices in the network:")
        print(dgboard_ip_list)




