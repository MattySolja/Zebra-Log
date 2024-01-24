import csv
import os
import shutil
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__, static_folder='C:/Users/owner/Desktop/qr')

entry_count = 0

@app.route('/endpoint', methods=['POST'])
def handle_data():
    global entry_count
    text_entry = request.form['textEntry']
    with open('C:/Users/owner/Desktop/qr/entries.csv', 'a', newline='') as file:
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
    with open('C:/Users/owner/Desktop/qr/entries.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            entries.append(row[0])
    cell_data = {f'cell{i+1}': entry for i, entry in enumerate(entries)}
    return render_template('amend.html', **cell_data)

@app.route('/submit_amendments', methods=['POST'])
def submit_amendments():
    global entry_count
    entries = [request.form[f'entry{i+1}'] for i in range(16)]
    with open('C:/Users/owner/Desktop/qr/entries.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for entry in entries:
            writer.writerow([entry])
    entry_count = 0
    return redirect(url_for('zebra'))

@app.route('/submit', methods=['POST'])
def submit():
    global entry_count
    shutil.copy('C:/Users/owner/Desktop/qr/entries.csv', 'C:/Users/owner/Desktop/qr/cellSerials.csv')
    os.remove('C:/Users/owner/Desktop/qr/entries.csv')
    entry_count = 0
    return redirect(url_for('zebra'))
    
@app.route('/restart', methods=['POST'])
def restart():
    global entry_count
    os.remove('C:/Users/owner/Desktop/qr/entries.csv')
    entry_count = 0
    return redirect(url_for('zebra'))    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)