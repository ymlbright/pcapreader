from frame_praser import frame_praser
import sys

class arp_frame(object):
	HardwareTypeTable = ["","Ethernet"]
	ProtocolTypeTable = {
		0x0800:"IP"
	}
	FrameJSON = """
		[
			{'name':'HTYPE','length':16},
			{'name':'PTYPE','length':16},
			{'name':'HLEN','length':8},
			{'name':'PLEN','length':8},
			{'name':'OPER','length':16},
			{'name':'SHA','length':48},
			{'name':'SPA','length':32},
			{'name':'THA','length':48},
			{'name':'TPA','length':32},
		]
	"""
	def __init__(self,data):
		self.data = frame_praser(FrameJSON,data)
