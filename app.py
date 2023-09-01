from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
import utils

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "u29h3e29h2e91h2e9w2jmqw09h23jq9hq"

@app.route('/')
def index():
    if 'username' in session:
            return f"Welcome, {session['username']}!"
    return "You are not logged in."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailorUsername']
        username = request.form['emailorUsername']
        password = request.form['password']

        user = db.get_user(connection, email, username)
        
        if user:
            if utils.is_password_match(password, user[5]):
                session['email'] = user[3]
                return redirect(url_for('index'))
            else:
                flash("Password dose not match", "danger")
                return render_template('login.html')
            
        else:
            flash("Invalid email", "danger")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email =request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, username)
        if user:
            flash("Username or Email already exists. Please try again !", "danger")
            return render_template('signup.html')
        
        else:
            db.add_user(connection,first_name,last_name,email, username, password)
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.init_db(connection)
    app.run(debug=True)