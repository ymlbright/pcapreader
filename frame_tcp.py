class tcp_frame(object):
    def __init__(self,data):
        self.src = (ord(data[0])<<8)+ord(data[1])
        self.dst = (ord(data[2])<<8)+ord(data[3])
        self.sequenceNumber = "0x"+data[4:8].encode('hex')
        self.acknowledgmentNumber = "0x"+data[8:12].encode('hex')
        self.headerLength = (ord(data[12])&0xf0)>>2
        self.flags = [];
        if(ord(data[12])&1):
            self.flags.append('NS')
        allFlag = ['CWR','ECE','URG','ACK','PSH','RST','SYN','FIN']
        for i in range(8):
            if(ord(data[13])&(1<<(7-i))):
                self.flags.append(allFlag[i])
        self.windowSize = (ord(data[14])<<8)+ord(data[15])
        self.checksum = "0x"+data[16:18].encode('hex')
        self.urgentPointer=(ord(data[18])<<8)+ord(data[19])
        self.data = data[self.headerLength:]

    def __repr__(self):
        return "[TCP?] src:%d,dst:%d,Header Length:%d bytes,Flag :%s,windowSize:%d,checksum:%s,urgentPointer:%d,data:\n%s"%(self.src,self.dst,self.headerLength,self.flags,self.windowSize,self.checksum,self.urgentPointer,self.data)