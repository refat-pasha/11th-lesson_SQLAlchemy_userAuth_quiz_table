from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),
                                      bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'),
                              self.password.encode('utf-8'))

class QuizSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.Column(db.JSON)  # Store answers as JSON for flexibility

    def __init__(self, user_id, answers):
        self.user_id = user_id
        self.answers = answers






with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('sign-up.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/dashboard')
        else:
            return render_template('login.html')

    return render_template('login.html')



@app.route('/dindex', methods=['POST', 'GET'])
def dindex():
    return render_template('dindex.html')




@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    email = session.get('email')
    if email:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)

    return redirect('/login')


@app.route('/dashboard-search', methods=['POST','GET'])
def dashboard_search():
    return render_template('dashboard-search.html')


@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    #questions = Quiz.query.all()
    return render_template('quiz.html')


@app.route('/publication', methods=['POST', 'GET'])
def publication():
    return render_template('publication.html')

@app.route('/publication-submit', methods=['POST','GET'])
def publication_submit():
    return render_template('publication-submit.html')


# def quiz_submit():
#     return render_template('submit.html')
@app.route('/submit', methods=['POST','GET'])
def quiz_submit():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            # Collect answers from the form
            answers = {
                'q1': request.form.get('q1'),
                'q2': request.form.get('q2'),
                'q3': request.form.get('q3'),
                'q4': request.form.get('q4'),
                'q5': request.form.get('q5')
            }

            # Save submission to the database
            quiz_submission = QuizSubmission(user_id=user.id, answers=answers)
            db.session.add(quiz_submission)
            db.session.commit()

            return redirect('/dashboard')
    return redirect('/login')

@app.route('/help', methods=['POST','GET'])
def help():
    return render_template('/help.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('email', None)
    return redirect('/login')







if __name__ == "__main__":
    app.run(debug=True)







