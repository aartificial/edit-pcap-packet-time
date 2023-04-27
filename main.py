from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.utils import PcapWriter

s = 'source/'
d = 'destination/'
time_increase = 31536000 + 1296000  # 1 year + 15 days

sources = []
for path, subdirs, files in os.walk(s):
    for name in files:
        sources = sources + [os.path.join(path, name)]

print("Editing packets:\n", sources)
for source in sources:
    filename = d + source
    output = PcapWriter(filename, append=True)
    packets = rdpcap(source)
    for packet in packets:
        print("Original time: ", packet.time)
        packet.time = packet.time + time_increase
        if packet[IP]:
            del packet[IP].chksum
        if packet[UDP]:
            del packet[UDP].chksum
        packet.show2()
        print("New time: ", packet.time)
        output.write(packet)

print("\nFinished editing packets")

