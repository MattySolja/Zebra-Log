import csv
import os
import shutil
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__, static_folder='')

entry_count = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/endpoint', methods=['POST'])
def handle_data():
    global entry_count
    text_entry = request.form['textEntry']
    with open('data/entries.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([text_entry])
    entry_count += 1

    if entry_count >= 16:
        return redirect(url_for('amend'))
    else:
        return redirect(url_for('zebra'))

@app.route('/zebra')
def zebra():
    return render_template('zebra.html', cell_number=entry_count+1)

@app.route('/amend')
def amend():
    entries = []
    with open('data/entries.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            entries.append(row[0])
    cell_data = {f'cell{i+1}': entry for i, entry in enumerate(entries)}
    return render_template('amend.html', **cell_data)

@app.route('/submit_amendments', methods=['POST'])
def submit_amendments():
    global entry_count
    entries = [request.form[f'entry{i+1}'] for i in range(16)]
    with open('data/entries.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for entry in entries:
            writer.writerow([entry])
    entry_count = 0
    return redirect(url_for('zebra'))

@app.route('/submit', methods=['POST'])
def submit():
    global entry_count
    shutil.copy('data/entries.csv', 'data/cellSerials.csv')
    os.remove('data/entries.csv')
    entry_count = 0
    return redirect(url_for('zebra'))
    
@app.route('/restart', methods=['POST'])
def restart():
    global entry_count
    os.remove('qr/data/entries.csv')
    entry_count = 0
    return redirect(url_for('zebra'))

@app.route('/valueChecker')
def value_checker():
    return render_template('serialCheck.html', message='')

@app.route('/checkvalue', methods=['POST'])
def check_value():
    submitted_value = request.form['value']
    with open('data/data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if submitted_value in row:
                count = 0
                builder = ""
                model = ""
                supplier = ""
                capacity = ""
                date = ""
                reference = ""
                neey = ""
                for item in row:
                    if count == 1:
                        builder = item
                    if count == 2:
                        model = item
                    if count == 3:
                        supplier = item
                    if count == 4:
                        capacity = item
                    if count == 21:
                        date = item
                    if count == 22:
                        reference = item
                    if count == 23:
                        neey = item
                    count += 1
                return render_template('serialCheck.html', message='Found', builder=builder, model=model, supplier=supplier, capacity=capacity, date=date, reference=reference, neey=neey)
    return render_template('serialCheck.html', message='Not found')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)