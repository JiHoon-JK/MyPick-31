from flask import Flask, render_template, session, url_for

app = Flask(__name__)

SECRET_KEY = 'apple'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.secret_key = 'Juni'
    app.run('localhost', port=9000, debug=True)