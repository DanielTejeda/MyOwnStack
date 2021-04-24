from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'estoesMUYsecreto'
db = SQLAlchemy (app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Question1(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qn_title = db.Column(db.String(100))
    qn_detail = db.Column(db.String(1000))
    answer1 = db.relationship('Answer1', backref='owner')
    #id_user = db.Column(db.Integer)

    def __init__(self, qn_title, qn_detail):
        self.qn_title = qn_title
        self.qn_detail = qn_detail

class Answer1(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ans_detail = db.Column(db.String(1000))
    id_qn = db.Column(db.Integer, db.ForeignKey('question1.id'))
    correct = db.Column(db.Integer)

    def __init__(self, ans_detail, id_qn, correct):
        self.ans_detail = ans_detail
        self.id_qn = id_qn
        self.correct = correct

# sentencia para crear todas las tablas
db.create_all()

class Question1Schema(ma.Schema):
    class Meta:
        fields = ("id", "qn_title", "qn_detail")

question_schema = Question1Schema()
questions_schema = Question1Schema(many=True)

class Answer1Schema(ma.Schema):
    class Meta:
        fields = ("id", "ans_detail", "id_qn","correct")

answer_schema = Answer1Schema()
answers_schema = Answer1Schema(many=True)

#####################################
# CONTROLADOR DE VISTAS
#####################################
@app.route('/', methods=["GET"])
def Index():
    #users = User.query.all()
    #questions = Question1.query.all()
    #answers = Answer1.query.all()

    #return render_template("index.html", users = users, questions = questions, answers = answers)
    return render_template("index.html")

@app.route('/about', methods=["GET"])
def About():
    return render_template("about.html")

@app.route('/answer/<id>', methods=["GET"])
def Answer(id):
    if "id_user" not in session:
        return redirect(url_for('Login'))

    qn = Question1.query.filter_by(id=id).first()
    return render_template("answer.html", qn = qn)

@app.route('/login', methods=["GET"])
def Login():
    return render_template("login.html")

@app.route('/question', methods=["GET"])
def Question():
    if "id_user" not in session:
        return redirect(url_for('Login'))
    return render_template("question.html")

@app.route('/register', methods=["GET"])
def Register():
    return render_template("register.html")

#####################################
# METODOS DE USUARIO
#####################################
@app.route('/registerUser', methods=["POST"])
def RegisterUser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    user_n = User.query.filter_by(name=name).first()
    user_e = User.query.filter_by(email=email).first()

    if user_n:
        error_message = "Ya existe un usuario con ese nombre"
        flash(error_message)
        return redirect(url_for('Register'))
    if user_e:
        error_message = "Ya existe un usuario con ese correo electrónico"
        flash(error_message)
        return redirect(url_for('Register'))
    
    contra_cifrada = generate_password_hash(password)
    #check_password_hash(psswdhash, password)
    contra_noCifrada = check_password_hash(contra_cifrada, password)
    print(contra_noCifrada)
    new_user = User(name, email, contra_cifrada)  # Creo un Usuario
    db.session.add(new_user)  # lo cargo a la BD
    db.session.commit() 

    user = User.query.filter_by(name=name).first()
    session["id_user"] = user.id

    return redirect(url_for('Index'))

@app.route('/loginUser', methods=["POST"])
def LoginUser():
    if "id_user" in session:
        return redirect(url_for('Index'))

    name = request.form['name']
    password = request.form['password']
    #contra_cifrada = generate_password_hash(password)

    user = User.query.filter_by(name=name).first()

    if user:
        if check_password_hash(user.password, password):
            session["id_user"] = user.id
            return redirect(url_for('Index'))
        error_message = "Usuario o contraseña incorrectos"
        flash(error_message)
        return redirect(url_for('Login'))
        #return render_template('login.html')
    error_message = "Usuario inexistente"
    flash(error_message)
    return redirect(url_for('Login'))
    #return render_template('login.html')

@app.route('/logoutUser', methods=["POST"])
def LogoutUser():
    if "id_user" in session:
        session.pop("id_user")
    return redirect(url_for('Index'))
    
@app.route('/ifUser', methods=["GET"])
def ifUser():
    response = "{\"value\":false}"
    if "id_user" in session:
        response = "{\"value\":true}"
    return response 

#####################################
# METODOS DE PREGUNTA
#####################################
@app.route('/pushQuestion', methods=["POST"])
def PushQuestion():
    title = request.form['qn_title']
    title = title.upper()
    detail = request.form['qn_detail']

    new_qn = Question1(title, detail)
    db.session.add(new_qn)
    db.session.commit()
    return redirect(url_for('Index'))

@app.route('/showQuestions', methods=["GET"])
def ShowQuestion():
    questions_q = Question1.query.all()
    questions = questions_schema.dump(questions_q)
    return jsonify(questions)

@app.route('/searchQuestion/', methods=["POST"])
def SearchQuestion():
    filter_q = request.form['qn_filter']
    filter_q = filter_q.upper()
    questions_query = Question1.query.all()
    print(type(questions_query))

    questions_q = filter (lambda qn : qn.qn_title.find(filter_q) != -1, questions_query)

    answers = Answer1.query.all()

    return render_template("index2.html", questions_q = questions_q, answers = answers)

    # INTERNTAR CON AJAX DSPS
    # questions = questions_schema.dump(questions_q)
    # return jsonify(questions)

#####################################
# METODOS DE RESPUESTA
#####################################
@app.route('/answer/pushAnswer/<id_qn>', methods=["POST"])
def PushAnswer(id_qn):
    detail = request.form['ans_detail']
    #id_qn = request.json['id_qn']

    new_ans = Answer1(detail, id_qn, 0)
    db.session.add(new_ans)
    db.session.commit()
    return redirect(url_for('Index'))

@app.route('/showAnswers', methods=["GET"])
def ShowAnswer():
    answers_q = Answer1.query.all()
    answers = answers_schema.dump(answers_q)
    return jsonify(answers)

@app.route('/checkAnswer/<id_ans>', methods=["POST"])
def CheckAnswer(id_ans):
    ans = Answer1.query.get(id_ans)
    if ans:
        ans.correct = 1
        db.session.commit()
        
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)