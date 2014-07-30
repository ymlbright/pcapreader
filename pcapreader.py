from struct import pack,unpack
from layertype import pEthernet
import os,sys

class Pcap(object):
	LayerDataTable = {
		1:pEthernet
	}

	def __init__(self, path=''):
		self.fp = 0
		self.header = {}
		self.packet = []
		self.data = []
		if path:
			self.open(path)

	def __del__(self):
		self.close()

	def __getitem__(self, key):
		if self.fp:
			if type(key) == int:
				try:
					layer_dispatch = self.LayerDataTable[self.header['LinkLayerHeaderType']]
					packet_data = layer_dispatch(self.packet[0],self.packet[key],self.data[key])
					return packet_data
				except KeyError:
					print "Unsupported content type."
				except:
					print "Unknow Error Pcap[class]-getitem. %s\n%s" % (sys.exc_info()[0],sys.exc_info()[1])
			else:
				raise KeyError
		else:
			print "No file opened."

	def open(self,path):
		if self.fp:
			self.header = {}
			self.packet = []
			self.data = []
			self.fp.close()
		try:
			self.fp = open(path,'rb')
			self.read_head()
			self.read_layer()
		except IOError:
			print "IOError: Can NOT open file [%s]." %  path
		except:
			print "Unknow Error in Pcap[class]-open. %s\n%s" % (sys.exc_info()[0],sys.exc_info()[1])

	def close(self):
		if self.fp:
			self.fp.close()

	def read_layer(self):
		if self.fp:
			self.fp.seek(24)
			file_size = os.fstat(self.fp.fileno()).st_size
			while self.fp.tell() < file_size:
				layer_header = {}
				header_readed = unpack('4i',self.fp.read(16))
				layer_header['TimeStamp'] = header_readed[0]
				layer_header['MicroSeconds'] = header_readed[1]
				layer_header['PacketLength'] = header_readed[2]
				layer_header['SavedLength'] = header_readed[3]
				self.packet.append(layer_header)
				layer_data = self.fp.read(layer_header['SavedLength'])
				self.data.append(layer_data)
		else:
			print "No file opened."

	def read_head(self):
		if self.fp:
			self.fp.seek(0)
			self.header['Magic'] = self.fp.read(4)
			self.header['MajorVer'] = unpack('i',self.fp.read(2)+'\x00\x00')[0]
			self.header['MinorVer'] =  unpack('i',self.fp.read(2)+'\x00\x00')[0]
			self.header['GTM1'] = self.fp.read(4)
			self.header['GTM2'] = self.fp.read(4)
			self.header['SnapshotMaxLen'] = unpack('i',self.fp.read(4))[0]
			self.header['LinkLayerHeaderType'] = unpack('i',self.fp.read(4))[0]
		else:
			print "No file opened."
	def __repr__(self):
		if self.fp:
			return "Pcap file version %d.%d, content type %d, file check %s"%( \
					self.header['MajorVer'], self.header['MinorVer'], \
					self.header['LinkLayerHeaderType'], \
					'pass' if '\xd4\xc3\xb2\xa1'==self.header['Magic'] else 'unpass')
		else:
			return "No file opened."

t = Pcap("74db9d6b62579fea4525d40e6848433f-net03.pcap")
i = 477
print t
print t[i]
print t[i].eth 
print t[i].eth.ipv4
print t[i].eth.ipv4.udp