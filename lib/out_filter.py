import db

def encrypter(acc_no):
	hashed=''
	enc={'0':'c','1':'d','2':'g','3':'h','4':'i','5':'j','6':'s','7':'t','8':'z','9':'a'}
	for i in acc_no:
		hashed+=enc[i]
	return hashed

def filter(msg,node,acc1):
	if node=='pin ok':
		msg=msg.replace("<balance>",str(db.bank_data[encrypter(acc1)]))
	return msg