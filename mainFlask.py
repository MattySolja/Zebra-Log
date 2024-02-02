from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/cells')
def add_cell():
    return render_template('addCells.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
