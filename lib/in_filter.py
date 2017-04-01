import json
import db

acc1='1'
acc2='1'
money=0

def encrypter(acc_no):
	hashed=''
	enc={'0':'c','1':'d','2':'g','3':'h','4':'i','5':'j','6':'s','7':'t','8':'z','9':'a'}
	for i in acc_no:
		hashed+=enc[i]
	return hashed

def validate_acc_no(acc_no):
	if not acc_no.isdigit(): return False
	elif encrypter(acc_no) in db.accounts: return True
	else: return False

def validate_balance(acc1,demand):
	return db.bank_data[encrypter(acc1)]>=demand

def transfer(acc1,acc2,money):
	db.bank_data[encrypter(acc1)]-=money
	db.bank_data[encrypter(acc2)]+=money

def filter(msg,node):
	
	global acc1
	global acc2
	global money

	if '-' in msg:

		print '--hyphens are not allowed--'
		return 'hey'

	elif node=='acc1 not ok' or node=='acc2 not ok' or node=='invalid acc no' or node=='balance check' or node=='fund transfer' or node=='acc1 ok':
		
		if node=='acc1 not ok' or node=='invalid acc no' or node=='balance check' or node=='fund transfer':
			acc1 = msg
		elif node=='acc1 ok' or node=='acc2 not ok':
			acc2 = msg

		if validate_acc_no(msg):
			return '-acc_ok-'
		elif msg.isdigit():
			return '-acc_not_ok-'
		else:
			return msg

	elif node=='ask pin' or node=='transfer possible':
		return '-pin_ok-'

	elif node=='acc2 ok':
		money=int(msg)
		if validate_balance(acc1,money):
			return '-yes-'
		elif msg.isdigit():
			return '-no-'
		else:
			return msg

	elif node=='pin ok again':
		transfer(acc1,acc2,money)

	elif node=='end':
		db.close()

	else:
		return msg
