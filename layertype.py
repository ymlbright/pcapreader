from struct import pack,unpack
import sys
from frame_ipv4 import ipv4_frame

class BasePcapData(object):
	def __init__(self, basehead, head):
		self.timestamp = [head['TimeStamp'], head['MicroSeconds']]
		self.len = head['SavedLength']
		self.caplen = head['PacketLength']
		self.basestamp =  [basehead['TimeStamp'], basehead['MicroSeconds']]
	
	def time(self):
		if self.timestamp[1]-self.basestamp[1] < 0 :
			return "%d.%d" % (self.timestamp[0]-self.basestamp[0]-1,0xf4240+self.timestamp[1]-self.basestamp[1])
		else:
			return "%d.%d" % (self.timestamp[0]-self.basestamp[0],self.timestamp[1]-self.basestamp[1])

class pEthernet(BasePcapData):
	EtherTypeTable= {
		0x0800:'Internet Protocol version 4 (IPv4)',
		0x0806:'Address Resolution Protocol (ARP)',
		0x0842:'Wake-on-LAN[3]',
		0x22F3:'IETF TRILL Protocol',
		0x6003:'DECnet Phase IV',
		0x8035:'Reverse Address Resolution Protocol',
		0x809B:'AppleTalk (Ethertalk)',
		0x80F3:'AppleTalk Address Resolution Protocol (AARP)',
		0x8100:'VLAN-tagged frame (IEEE 802.1Q) & Shortest Path Bridging IEEE 802.1aq[4]',
		0x8137:'IPX',
		0x8138:'IPX',
		0x8204:'QNX Qnet',
		0x86DD:'Internet Protocol Version 6 (IPv6)',
		0x8808:'Ethernet flow control',
		0x8809:'Slow Protocols (IEEE 802.3)',
		0x8819:'CobraNet',
		0x8847:'MPLS unicast',
		0x8848:'MPLS multicast',
		0x8863:'PPPoE Discovery Stage',
		0x8864:'PPPoE Session Stage',
		0x8870:'Jumbo Frames[2]',
		0x887B:'HomePlug 1.0 MME',
		0x888E:'EAP over LAN (IEEE 802.1X)',
		0x8892:'PROFINET Protocol',
		0x889A:'HyperSCSI (SCSI over Ethernet)',
		0x88A2:'ATA over Ethernet',
		0x88A4:'EtherCAT Protocol',
		0x88A8:'Provider Bridging (IEEE 802.1ad) & Shortest Path Bridging IEEE 802.1aq[5]',
		0x88AB:'Ethernet Powerlink[citation needed]',
		0x88CC:'Link Layer Discovery Protocol (LLDP)',
		0x88CD:'SERCOS III',
		0x88E1:'HomePlug AV MME[citation needed]',
		0x88E3:'Media Redundancy Protocol (IEC62439-2)',
		0x88E5:'MAC security (IEEE 802.1AE)',
		0x88F7:'Precision Time Protocol (IEEE 1588)',
		0x8902:'IEEE 802.1ag Connectivity Fault Management (CFM) Protocol / ITU-T Recommendation Y.1731 (OAM)',
		0x8906:'Fibre Channel over Ethernet (FCoE)',
		0x8909:'Security Group Tag Ethernet (SGT)[6]',
		0x8914:'FCoE Initialization Protocol',
		0x8915:'RDMA over Converged Ethernet (RoCE)',
		0x892F:'High-availability Seamless Redundancy (HSR)',
		0x9000:'Ethernet Configuration Testing Protocol[7]',
		0x9100:'Q-in-Q',
		0xCAFE:'Veritas Low Latency Transport (LLT)[8] for Veritas Cluster Server'
	}
	EtherTypeDispatchTable = {
		0x0800: ipv4_frame
	}
	def __init__(self, basehead, head, body):
		super(pEthernet,self).__init__(basehead,head)
		self.dst = body[0:6]
		self.src = body[6:12]
		self.type = (ord(body[12])<<8) + ord(body[13])
		try:
			dispatch_fun = self.EtherTypeDispatchTable[self.type]
			self.eth = dispatch_fun(body[14:])
		except KeyError:
			self.eth = body[14:]
		except:
			print "Unknow Error in pEthernet[class]-init. %s\n%s" % (sys.exc_info()[0],sys.exc_info()[1])

	def __repr__(self):
		return "Ethernet: %02x:%02x:%02x:%02x:%02x:%02x -> %02x:%02x:%02x:%02x:%02x:%02x, EtherType: %s(%04x), Size: %d"%( \
			ord(self.src[0]), ord(self.src[1]), ord(self.src[2]),
			ord(self.src[3]), ord(self.src[4]), ord(self.src[5]),
			ord(self.dst[0]), ord(self.dst[1]), ord(self.dst[2]), 
			ord(self.dst[3]), ord(self.dst[4]), ord(self.dst[5]), 
			self.EtherTypeTable[self.type] if self.type in self.EtherTypeTable.keys() else 'Unknown',
			self.type, self.len)
