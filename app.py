from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create a login manager instance
login_manager = LoginManager()
login_manager.init_app(app)

# User database
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'},
    'user3': {'password': 'password3'}
}

# User class for Flask-Login
class User(UserMixin):
    pass

# User loader function for Flask-Login
@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            user = User()
            user.id = username
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Username already exists')
        users[username] = {'password': password}
        return redirect('/login')
    else:
        return render_template('register.html')

# Home page route
@app.route('/')
@login_required
def home():
    return render_template('home.html', username=session.get('username'))

if __name__ == '__main__':
    app.run()
