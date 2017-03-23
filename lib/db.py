import os
import json

def close():
	file = open(os.getcwd()+'/res/database.json','w')
	json.dump(bank_data,file)
	file.close()

file = open(os.getcwd()+'/res/database.json','r')
bank_data = json.load(file)

accounts=[]
for accountnumber in bank_data:
	accounts.append(accountnumber)