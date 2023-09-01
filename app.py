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
            return render_template("index.html")
        



@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute") 
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
@limiter.limit("5 per minute") 
def sign_up():
    if request.method == 'POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        email =request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = db.get_user(connection, email,username)
        if user:
            flash("Username or Email already exists. Please try again !", "danger")
            return render_template('signup.html')
        
        else:
            db.add_user(connection,first_name,last_name,email, username, password)
            return redirect(url_for('login'))

    return render_template('signup.html')



@app.route('/upload-restaurant', methods=['GET', 'POST'])
@limiter.limit("10 per minute") 
def uploadrestaurant():

    if request.method == 'POST':
        restaurantImage = request.files['image']
        if not restaurantImage or restaurantImage.filename == '':
            flash("Image Is Required", "danger")
            return render_template("upload-restaurant.html")

        if not validators.allowed_file(restaurantImage.filename) or not validators.allowed_file_size(restaurantImage):
            flash("Invalid File is Uploaded", "danger")
            return render_template("upload-restaurant.html")

        title = request.form['title']
        description = request.form['description']
    
        image_url = f"uploads/{restaurantImage.filename}"
        restaurantImage.save("assets/images/" + image_url)
        user_id = session['user_id']
        db.add_restaurant(connection, user_id, title, description,image_url)
        return redirect(url_for('index'))
    return render_template('upload-restaurant.html')


app.route('/restaurant/<restaurant_id>')
def getrestaurant(restaurant_id):
	restaurant = db.get_restaurant(connection, restaurant_id)
	














@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.init_db(connection)
    app.run(debug=True)
    