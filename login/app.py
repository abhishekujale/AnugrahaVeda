from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Assuming you have a form with fields 'username' and 'password'
        username = request.form['username']
        password = request.form['password']
        # Check if the credentials are valid (you should have your own validation logic here)
        if username == 'your_username' and password == 'your_password':
            # Save the username in the session
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')
def is_logged_in():
    return 'username' in session

@app.route('/')
def index():
    if not is_logged_in():
        return redirect('/login')
    # Render your protected page
    return render_template('index.html', username=session['username'])
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
