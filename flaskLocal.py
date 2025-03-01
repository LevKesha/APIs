from flask import Flask

# Create a Flask application instance
app = Flask(__name__)

if __name__ == '__main__':
    app.run(port=5050)