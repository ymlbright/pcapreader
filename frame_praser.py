from json import loads
from math import ceil,floor
'''
[
	{
		name:xxx,
		length:xx,
	},
	{
		name:xxx,
		length:[xx,xx,xx,xx]
	},
	name3:{
		name:xxx,
		length:xxx,
	}
]
'''

def frame_praser(json,data):
	format = loads(json)
	out = {}
	ptr_f = 0
	ptr_b = 0
	for item in format:
		if type(item['length']) == list:
			ptr_b += len(item['length'])
		else:
			ptr_b += item['length']
		re = 0
		for i in range(int(floor(ptr_f/8.0)),int(ceil(ptr_b/8.0))):
			mask = 1 << (7-ptr_f%8)
			while mask and ptr_f<ptr_b:
				if ord(data[i]) & mask:
					re = re * 2 + 1
				else:
					re *=2
				mask = mask >> 1
				ptr_f +=1
		if type(item['length']) == list:
			out[item['name']] = ""
			for j in range(0,len(item['length'])):
				if re & 2**j:
					out[item['name']] = out[item['name']] + " | " + str(item['length'][len(item['length'])-j])
			out[item['name']] = out[item['name']][3:]
		else:
			o = ""
			while re:
				o = chr(re&0xff) + o
				re = re >> 8
			out[item['name']] = o
	return out


js = '[{"name":"x0","length":4},{"name":"x1","length":8},{"name":"x2","length":24},{"name":"x3","length":[1,2,3,4,5,6,7]}]'
test = "5146243233145234533234022a0a0a960a000068dbcb0035004e1f3fb61a01000001000000000000296161616161327161616161616161616161616161616161612d303031653333653964656362666362340662616467757903636f6d0000100001"
test = test.decode('hex')
print frame_praser(js,test)