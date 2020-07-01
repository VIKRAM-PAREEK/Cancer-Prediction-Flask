from flask import Flask,render_template,request, redirect , url_for
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import csv

app = Flask(__name__)

@app.route('/',methods= ['GET','POST'])
def home():	
	return render_template('frontpage.html')

@app.route('/userinput')
def user_input():
	return render_template('userinput.html')

@app.route('/results', methods= ['GET','POST'])

def result():
	name = ''
	val = ''
	d = {} #for storing the user input
	
	if request.method == 'POST':
		val = request.form
	if request.form.get('username')!=None:
		name = request.form.get('username')
		for key, value in val.items():
			print(key," ", value)
			if key!='username':
				d[key] = value
		print(d)

		#training our model
		seer = pd.read_csv("C:\\Users/home/Desktop/SEER_CANCER_PREDICTION/SEER_CANCER_PREDICTION/data.csv",header = 0)
		
		seer.drop('Unnamed: 32',axis=1,inplace=True)
		seer.drop(['id'], inplace=True, axis=1)
		seer['diagnosis'] = seer['diagnosis'].map({'M':1,'B':0})
		y=seer.diagnosis.values
		seer.drop(['diagnosis'], inplace=True, axis=1)

		x=seer.values

		scaler=StandardScaler()
		x=scaler.fit_transform(x)
		x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.29,random_state=0)

		#random forest model
		RF= RandomForestClassifier(max_depth=5,n_estimators=100)
		RF.fit(x_train,y_train)
		RF.score(x_train,y_train)
		RF.score(x_test,y_test)
		RF.score(x,y)

		y_predict=RF.predict(x_test)
		print(y_predict)

		
		#testing with uservalues
		with open('mycsv.csv', 'w+', newline='') as f:
			fieldnames = ['rmean', 'tmean', 'pmean', 'amean', 'smean', 'cmpmean', 'conmean', 'cpmean', 'symean', 'fdmean', 'rse', 'tse', 'pse', 'ase', 'smse', 'cmpse', 'cnse', 'cpse', 'syse', 'fdse', 'radw', 'textw', 'periw', 'areaw', 'smtw', 'cmpw', 'concw', 'cpw', 'symmw', 'fdw']
			thewriter = csv.DictWriter(f, fieldnames=fieldnames)

			thewriter.writeheader()
			thewriter.writerow(d)
		test=pd.read_csv("mycsv.csv",header = 0)
		
		#making the prediction
		z=test
		z=scaler.transform(z)
		submission_predict=RF.predict(z)
		print(submission_predict)
		prediction = '' 		
		if submission_predict[0]==1:
			prediction = "It's Malignant!! Please consult a Doctor immediately"
		else:
			prediction = "It's Benign,The tumour isn't cancerous"
		return render_template('results.html',name=name,prediction = prediction)


	
app.run(debug = True)