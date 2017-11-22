from flask import Flask, render_template, request, url_for, redirect

from flask.ext.sqlalchemy import SQLAlchemy

from google.appengine.ext import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


class Tasks(db.Model):
	__tablename__ = 'tasks'
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String)
	descricao = db.Column(db.String)
	prioridade = db.Column(db.String)
	usuario = db.Column(db.String)

	def __init__(self, nome, descricao, prioridade, usuario):
		self.nome = nome
		self.descricao = descricao
		self.prioridade = prioridade
		self.usuario = usuario

db.create_all()

@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/")
@app.route("/cadastrar")
def cadastrar():
	return render_template("cadastro.html")


def voltar():
	return render_template("home")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
	if request.method == "POST":
		nome = (request.form.get("nome"))
		descricao = (request.form.get("descricao"))
		prioridade = (request.form.get("prioridade"))
		usuario = (request.form.get("usuario"))

		if nome and descricao and prioridade and usuario:
			p = Tasks(nome, descricao, prioridade, usuario)
			db.session.add(p)
			db.session.commit()

	return redirect(url_for("home"))

@app.route("/lista")
def lista():
	tasks = Tasks.query.all()
	return render_template("lista.html", tasks=tasks)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
	tasks = Tasks.query.filter_by(_id=id).first()
	if request.method == "POST":
		nome = (request.form.get("nome"))
		descricao = (request.form.get("descricao"))
		prioridade = (request.form.get("prioridade"))
		usuario = (request.form.get("usuario"))

		if nome and descricao and prioridade and usuario:
			tasks.nome = nome
			tasks.descricao= descricao
			tasks.prioridade = prioridade
			tasks.usuario = usuario
			db.session.commit()

	return render_template("atualizar.html", tasks=tasks)

@app.route("/excluir/<int:id>")
def excluir(id):
	tasks = Tasks.query.filter_by(_id=id).first()

	db.session.delete(tasks)
	db.session.commit()

	tasks = Tasks.query.all()
	return render_template("lista.html", tasks=tasks)

if __name__ == "__main__":
	app.run(debug=True)
