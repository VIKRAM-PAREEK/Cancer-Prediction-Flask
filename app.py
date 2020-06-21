from flask import Flask,render_template,request


app = Flask(__name__)

@app.route('/',methods= ['GET','POST'])
def home():	
	return render_template('frontpage.html')

@app.route('/results', methods= ['GET','POST'])

def result():
	name = ''
	val = ''
	if request.method == 'POST':
 		val = request.form
 		name = request.form.get('username')
	return render_template('results.html',name = name)

app.run(debug = True)