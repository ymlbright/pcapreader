from struct import pack,unpack
from frame_udp import udp_frame
import sys

class ipv4_frame(object):
	ProtocolTable = [
		'HOPOPT', 'ICMP', 'IGMP', 'GGP', 'IP-in-IP', 'ST', 'TCP', 'CBT',
		'EGP', 'IGP', 'BBN-RCC-MON', 'NVP-II', 'PUP', 'ARGUS', 'EMCON',
		'XNET', 'CHAOS', 'UDP', 'MUX', 'DCN-MEAS', 'HMP', 'PRM', 'XNS-IDP',
		'TRUNK-1', 'TRUNK-2', 'LEAF-1', 'LEAF-2', 'RDP', 'IRTP', 'ISO-TP4',
		'NETBLT', 'MFE-NSP', 'MERIT-INP', 'DCCP', '3PC', 'IDPR', 'XTP', 'DDP', 
		'IDPR-CMTP', 'TP++', 'IL', 'IPv6', 'SDRP', 'IPv6-Route', 'IPv6-Frag', 
		'IDRP', 'RSVP', 'GRE', 'MHRP', 'BNA', 'ESP', 'AH', 'I-NLSP', 'SWIPE', 
		'NARP', 'MOBILE', 'TLSP', 'SKIP', 'IPv6-ICMP', 'IPv6-NoNxt', 'IPv6-Opts', 
		'-', 'CFTP', '-', 'SAT-EXPAK', 'KRYPTOLAN', 'RVD', 'IPPC', '-', 
		'SAT-MON', 'VISA', 'IPCU', 'CPNX', 'CPHB', 'WSN', 'PVP', 'BR-SAT-MON', 
		'SUN-ND', 'WB-MON', 'WB-EXPAK', 'ISO-IP', 'VMTP', 'SECURE-VMTP', 'VINES', 
		'TTP', 'IPTM', 'NSFNET-IGP', 'DGP', 'TCF', 'EIGRP', 'OSPF', 'Sprite-RPC', 
		'LARP', 'MTP', 'AX.25', 'IPIP', 'MICP', 'SCC-SP', 'ETHERIP', 'ENCAP', '-', 
		'GMTP', 'IFMP', 'PNNI', 'PIM', 'ARIS', 'SCPS', 'QNX', 'A/N', 'IPComp', 
		'SNP', 'Compaq-Peer', 'IPX-in-IP', 'VRRP', 'PGM', '-', 'L2TP', 'DDX', 
		'IATP', 'STP', 'SRP', 'UTI', 'SMP', 'SM', 'PTP', 'IS-IS over IPv4', 
		'FIRE', 'CRTP', 'CRUDP', 'SSCOPMCE', 'IPLT', 'SPS', 'PIPE', 'SCTP', 
		'FC', 'RSVP-E2E-IGNORE', 'Mobility Header', 'UDPLite', 'MPLS-in-IP', 
		'manet', 'HIP', 'Shim6', 'WESP', 'ROHC',
	]
	ProtocolDispatchTable = {
		17:udp_frame
	}
	def __init__(self,data):
		if ord(data[0])&0xf0 == 0x40:  # is ipv4 frame
			self.IHL = (ord(data[0])&0x0f)
			self.DSCP = ord(data[1])&0xfc >> 2
			self.ECN = ord(data[1])&0x3
			self.len = (ord(data[2])<<8) + ord(data[3])
			self.Identification = unpack('2c', data[4:6])[0]
			self.Flags = ord(data[6])&0xe0 >> 5
			self.FragmentOffset = ((ord(data[6])&0x1f)<<8)+ord(data[7])
			self.TTL = ord(data[8])
			self.Protocol = ord(data[9])
			self.HeaderCheck = (data[10:12]==self.heder_check(data))
			self.src = data[12:16] 
			self.dst = data[16:20]
			self.Option = data[20:self.IHL*4]
			try:
				dispatch_fun = self.ProtocolDispatchTable[self.Protocol]
				self.ipv4 = dispatch_fun(data[self.IHL*4:])
			except KeyError:
				self.ipv4 = data[self.IHL*4:]
			except:
				print "Unknow Error in ipv4_frame[class]-init. %s\n%s" % (sys.exc_info()[0],sys.exc_info()[1])
		else:
			raise TypeError

	def heder_check(self,data):
		high = sum(ord(x) for x in data[0:10:2]) + sum(ord(x) for x in data[12:20:2])
		low = sum(ord(x) for x in data[1:10:2]) + sum(ord(x) for x in data[13:20:2])
		csum = (high<<8) +low
		csum = (csum&0xffff) + ((csum&0xff0000)>>16)
		csum = csum ^ 0xffff
		return chr((csum>>8)&0xff)+chr(csum&0xff)

	def __repr__(self):
		if self.len:
			return "[Ipv4%s]: %d.%d.%d.%d -> %d.%d.%d.%d, Protocol: %s(%d), Size: %d" % ( \
				'.' if self.HeaderCheck else '!',
				ord(self.src[0]),ord(self.src[1]),ord(self.src[2]),ord(self.src[3]),
				ord(self.dst[0]),ord(self.dst[1]),ord(self.dst[2]),ord(self.dst[3]),
				self.ProtocolTable[self.Protocol] if self.Protocol<0x8f else 'Unknown',
				self.Protocol, self.len)
		else:
			return "None"

if __name__ =="__main__":
	test = "450000620001000040115b830a0a0a960a000068dbcb0035004e1f3fb61a01000001000000000000296161616161327161616161616161616161616161616161612d303031653333653964656362666362340662616467757903636f6d0000100001"
	test = test.decode('hex')
	t = ipv4_frame(test)
	print t.ipv4

