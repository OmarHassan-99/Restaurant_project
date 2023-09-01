from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
import utils
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import validators

app = Flask(__name__)
connection = db.connect_to_database()
app.secret_key = "u29h3e29h2e91h2e9w2jmqw09h23jq9hq"
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["10 per minute"])



@app.route('/index')
def index():
    #if 'username' in session:
        return render_template('index.html', restaurants = db.get_all_restaurants(connection))
    
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailorUsername']
        username = request.form['emailorUsername']
        password = request.form['password']

        user = db.get_user(connection, email, username)
        
        if db.seed_admin_user(username,password):
            session['username']=username
            return redirect(url_for('uploadRest')) 
        
        
        
        
        
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
        
        if not utils.is_strong_password(password):
                flash("Sorry You Entered a weak Password Please Choose a stronger one", "danger")
                return render_template('signup.html')

        user = db.get_user(connection, email,username)
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




	
@app.route('/upload-restaurant', methods=['GET', 'POST'])
def uploadRest():
    if 'username' in session:
        if session['username'] == 'admin':
            if request.method == 'POST':

                title = request.form['title']
                description = request.form['description']
                restaurant_image = request.files['image']
                imagePath = f"static/uploads/{restaurant_image.filename}"
                restaurant_image.save(imagePath)
                db.add_restaurant(connection, title, description, imagePath)
                restaurants = db.get_all_restaurants(connection)
                
                if not restaurants:
                    flash("No data found..", "danger")
                return redirect(url_for('index'))
            
            return render_template('upload-restaurant.html')
        else:
            flash('Unauthorized user..', 'danger')
            return redirect(url_for('index'))
        
        
        
        
        









if __name__ == '__main__':
    db.init_db(connection)
    db.init_restaurant(connection)
    app.run(debug=True)
    