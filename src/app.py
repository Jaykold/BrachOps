from flask import Flask
import config

app = Flask(__name__)

# Use configuration in your application
app.config['DEBUG'] = config.DEBUG
app.config['SECRET_KEY'] = config.SECRET_KEY

@app.route('/')
def hello():
    return f"Debug mode is {'on' if config.DEBUG else 'off'}. Log level is {config.LOG_LEVEL}."

if __name__ == '__main__':
    app.run(debug=config.DEBUG)