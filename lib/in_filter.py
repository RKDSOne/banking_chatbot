import json
import db

acc1='1'
acc2='1'
money=0

def validate_acc_no(acc_no):
	if acc_no in db.accounts: return True
	else: return False

def validate_balance(acc1,demand):
	return db.bank_data[acc1]>=demand

def transfer(acc1,acc2,money):
	db.bank_data[acc1]-=money
	db.bank_data[acc2]+=money

def filter(msg,node):
	
	global acc1
	global acc2
	global money

	if '-' in msg:

		print '--hyphens are not allowed--'
		return 'hey'

	elif node=='invalid acc no' or node=='balance check' or node=='fund transfer' or node=='acc1 ok':
		
		if node=='balance check' or node=='fund transfer':
			acc1 = msg
		elif node=='acc1 ok':
			acc2 = msg

		if validate_acc_no(msg):
			return '-acc_ok-'
		else:
			return '-acc_not_ok-'

	elif node=='ask pin' or node=='transfer possible':
		return '-pin_ok-'

	elif node=='acc2 ok':
		money=int(msg)
		if validate_balance(acc1,money):
			return '-yes-'
		else:
			return '-no-'

	elif node=='pin ok again':
		transfer(acc1,acc2,money)

	elif node=='end':
		db.close()

	else:
		return msg
