
class domain_frame(object):
	def __init__(self,data):
		self.ID = (ord(data[0])<<8) + ord(data[1])
		self.Flag = data[2:4]
		self.QuestionNum = (ord(data[4])<<8) + ord(data[5])
		self.AnswerNum = (ord(data[6])<<8) + ord(data[7])
		self.AuthorityNum = (ord(data[8])<<8) + ord(data[9])
		self.AdditionalNum = (ord(data[10])<<8) + ord(data[11])
		tlen = data.find('\x00',12)
		self.Queries = data[12:tlen]

	def read_head(self,data):
		answer = {}
		tlen = data.find('\x00')
		answer['Name'] = data[0:tlen]
		

