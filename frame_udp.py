from struct import pack,unpack
from frame_domain import domain_frame
import sys

class udp_frame(object):
	PortProtocolDispatch = {
		53 : domain_frame
	}
	def __init__(self,data):
		self.src = (ord(data[0])<<8) + ord(data[1])
		self.dst = (ord(data[2])<<8) + ord(data[3])
		self.len = (ord(data[4])<<8) + ord(data[5])
		self.Check = data[6:8]
		try:
			dispatch_fun = self.PortProtocolDispatch[self.dst]
			self.udp = dispatch_fun(data[8:])
		except KeyError:
			self.udp = data[8:]
		except:
			print "Unknow Error in udp_frame[class]-init. %s\n%s" % (sys.exc_info()[0],sys.exc_info()[1])

	def udp_check(self):
		return '?'

	def __repr__(self):
		if self.len:
			return "[UDP%s]: %d -> %d, Size: %d" %( \
				'?' if not self.Check else self.udp_check(),
				self.src, self.dst, self.len)