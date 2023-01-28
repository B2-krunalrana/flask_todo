from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
	sno=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(200),nullable=False)
	desc=db.Column(db.String(600),nullable=False)
	date=db.Column(db.DateTime,default=datetime.utcnow)

	def __repr__(self) -> str:
		return f'{self.sno} ------- {self.title}------'


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/db_creat')
def db_creat():	
	db.create_all()
	return '<-------- database update succesfully ------------->'

# @app.route('/db_del')
# def db_del():
# 	obj=Todo.query.all()
# 	# db.session.delete(a)
# 	db.session.delete(obj)
# 	db.session.commit()
# 	return '<-------- database DELETE succesfully ------------->'


@app.route('/todo',methods=['GET','POST'])
def todo():
	if request.method=='POST':
		title=request.form['title']
		desc=request.form['desc']
		if len(title)==0:
			title="Please Entre value"
			desc="None"
		todo=Todo(title=title,desc=desc)
		db.session.add(todo)
		db.session.commit()
	allTodo=Todo.query.all()

	return render_template('db_display.html',allTodo=allTodo)



@app.route('/update/<int:sno>')
def db_update(sno):
	alltodo=Todo.query.all()

	return 'check this one db_update'


@app.route('/delete/<int:sno>')
def db_delete(sno):
	alltodo=Todo.query.filter_by(sno=sno).first()
	db.session.delete(alltodo)
	db.session.commit()
	return redirect("/todo")



if __name__ == '__main__':
	app.run(debug=True,port=8000)
	
