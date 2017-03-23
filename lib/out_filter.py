import db

def filter(msg,node,acc1):
	if node=='pin ok':
		msg=msg.replace("<balance>",str(db.bank_data[acc1]))
	return msg