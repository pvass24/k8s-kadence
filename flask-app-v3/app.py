from flask import Flask, render_template_string
import os
from prometheus_client import Counter, generate_latest
from flask import Response

app = Flask(__name__)

# Prometheus metrics
c = Counter('myflaskapp_requests_total', 'Total number of requests to the Flask app')

@app.route('/')
def hello():
    username = os.environ.get('USERNAME', 'User')
    bg_color = os.environ.get('BG_COLOR', 'lightblue')
    font_color = os.environ.get('FONT_COLOR', 'white')
    return render_template_string('''
        <html>
            <head>
                <title>K8's Kadence</title>
            </head>
            <body style="background-color: {{ bg_color }}; color: {{ font_color }};">
                <h1>Hello {{ username }} welcome to K8’s Kadence!</h1>
            </body>
        </html>
    ''', username=username, bg_color=bg_color, font_color=font_color)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

