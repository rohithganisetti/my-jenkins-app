from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "Welcome to AWS ECR via Jenkins Pipeline - Auto Updated09"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)