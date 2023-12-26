from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def hello():
    username = os.environ.get('USERNAME', 'User')
    return render_template_string('''
        <html>
            <head>
                <title>K8's Kadence</title>
            </head>
            <body style="background-color: lightblue; color: white;">
                <h1>Hello {{ username }} welcome to K8’s Kadence!</h1>
            </body>
        </html>
    ''', username=username)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

