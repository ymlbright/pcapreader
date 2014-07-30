
class domain_frame(object):
	def __init__(self,data):
		self.ID = (ord(data[0])<<8) + ord(data[1])
		self.Flag = data[2:4]
		self.QuestionNum = (ord(data[4])<<8) + ord(data[5])
		self.AnswerNum = (ord(data[6])<<8) + ord(data[7])
		self.AuthorityNum = (ord(data[8])<<8) + ord(data[9])
		self.AdditionalNum = (ord(data[10])<<8) + ord(data[11])
		self.Queries = []
		self.Answers = []
		self.Authorities = []
		self.Additionnals = []
		tlen = 12
		i = self.QuestionNum
		while i:
			addlen,answer = self.read_head(data[tlen:])
			tlen += addlen
			self.Queries.append(answer)
			i -= 1
		tlen = self.head_paser(self.Answers, self.AnswerNum, tlen, data)
		tlen = self.head_paser(self.Authorities, self.AuthorityNum, tlen, data)
		tlen = self.head_paser(self.Additionnals, self.AdditionalNum, tlen, data)

	def read_head(self,data):
		answer = {}
		tlen = data.find('\x00')
		answer['Name'] = data[0:tlen]
		answer['Type'] = data[tlen+1:tlen+3]
		answer['Class'] = data[tlen+3:tlen+5]
		return tlen+5,answer

	def head_paser(self, arr, count, tlen, data):
		while count:
			addlen,answer = self.read_head(data[tlen:])
			tlen += addlen
			answer['TimeToLive'] = (ord(data[tlen])<<24) + (ord(data[tlen+1])<<16) + (ord(data[tlen+2])<<8) + ord(data[tlen+3]) 
			tlen += 4
			answer['DataLength'] = (ord(data[tlen])<<8) + ord(data[tlen+1]) 
			answer['Data'] = data[tlen+2:tlen+2+answer['DataLength']]
			tlen += 2+answer['DataLength']
			arr.append(answer)
			count -= 1
		return tlen

	def __repr__(self):
		return "[DNS] %s, Queries: %d, Answers: %d, Authorities: %d, Additionnals: %d"%( \
			self.Queries[0]['Name'].replace('\x03','.').replace('\x06','.'),
			self.QuestionNum, self.AnswerNum, self.AuthorityNum,
			self.AdditionalNum)

