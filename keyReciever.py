from flask import Flask, request, render_template
import pyautogui

app = Flask(__name__)

@app.route('/type', methods=['POST'])
def type_text():
    text = request.form.get('text')
    print(text)
    pyautogui.typewrite(text, interval=0.01)  # Reduce delay between key presses
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
