from flask import Flask, render_template_string, Response
from prometheus_client import Counter, Histogram, generate_latest  # Import generate_latest
import os
import time

app = Flask(__name__)

# Prometheus metrics
request_count = Counter('flask_app_request_count', 'Total number of requests')
request_duration = Histogram('flask_app_request_duration_seconds', 'Request duration in seconds')

@app.route('/')
def hello():
    username = os.environ.get('USERNAME', 'User')
    request_count.inc()  # Increment the request count
    start_time = time.time()

    # Simulate some processing time (you can remove this in production)
    time.sleep(0.1)

    end_time = time.time()
    request_duration.observe(end_time - start_time)  # Observe the request duration

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

@app.route('/metrics')
def metrics():
    # Serve Prometheus metrics
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

