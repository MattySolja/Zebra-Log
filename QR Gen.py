import segno
from PIL import Image , ImageDraw , ImageFont
import os
import csv
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
import subprocess

process = subprocess.Popen(["python", "pyserver.py"])

dropdownShift = 0.25
bigButtonHeight = 0.9

def close_window():
    process.terminate()
    window.destroy()

def genQR():
    now = datetime.now()
    serial = (str(now)).replace(" ","").replace(":","").replace("-","").replace(".","")

    textTop = "OGP"
    textBottom = serial

    qrcode = segno.make_qr(str(serial))
    qrcode.save(
        "current.png",
        scale=10,
        border=2,
    )

    img = Image.open("current.png")
    bg = Image.new("RGB", (580, 290), (255, 255, 255))

    bg.paste(img, (0, 0))
    bg.save("combined.png")
    bg = Image.open("combined.png")

    draw = ImageDraw.Draw(bg)
    fontTop = ImageFont.truetype("arial.ttf", 122)
    fontBottom = ImageFont.truetype("arial.ttf", 30)

    draw.text((275, 75), textTop, fill="black", font=fontTop)
    draw.text((25, 250), textBottom, fill="black", font=fontBottom)

    bg.save("combined.png")

    os.system(f'start /min "" "combined.png" /print')

    # Get the data from the forms
    data1 = builder.get()
    data2 = model.get()
    data3 = supplier.get()
    data4 = capacity.get()
    data5 = job.get()

    cell_serials = []
    with open('cellserials.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cell_serials.append(row[0])

    # Write the data to a file
    with open('data.csv', 'a') as file:
        file.write(f'{serial},{data1},{data2},{data3},{data4},{cell_serials},{now},{data5}\n')

    # Continue with the existing code...

def refresh():
    # Read the CSV file
    cell_serials = []
    with open('cellserials.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cell_serials.append(row[0])  # Change this if the serial number is not in the first column

    # Update the buttons
    for i, cell in enumerate(cells):
        cell['text'] = cell_serials[i]


# Create an empty list to store the cell serials
cell_serials = []

# Open the CSV file
with open('C:/Users/owner/Desktop/qr/cellSerials.csv', 'r') as file:
    # Create a CSV reader
    reader = csv.reader(file)

    # Iterate over the rows in the CSV file
    for row in reader:
        # Add the row to the list
        cell_serials.append(row[0])  # Change this if the serial number is not in the first column

# Create the main window
window = tk.Tk()
window.title("QR Generator")

# Open the window in fullscreen
window.attributes('-fullscreen', True)

# Set the window size
window_width = 300
window_height = 200
window.geometry(f"{window_width}x{window_height}")

# Calculate position for centering the window
positionTop = int(window.winfo_screenheight() / 2 - window_height / 2)
positionRight = int(window.winfo_screenwidth() / 2 - window_width / 2)

# Position the window
window.geometry(f"+{positionRight}+{positionTop}")

# Create a frame in the window to hold other widgets
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# Create a frame for the buttons
cellFrame = tk.Frame(frame)
cellFrame.place(relx=0.65, rely=0.05, relwidth=0.3, relheight=0.8)

# Calculate the relative font size
relative_font_size = int(window_width / 15)  # Adjust the divisor to get the desired font size

# Set the font
font = ("Arial", relative_font_size)

# Create a 2x8 grid of buttons
cells = []
for i in range(len(cell_serials)):
    cell = tk.Button(cellFrame, text=cell_serials[i], bg="blue", fg="white", height=4, width=22)
    row = (7 - i) % 8 if i < 8 else (15 - i) % 8
    column = 0 if i < 8 else 1
    cell.grid(row=row, column=column)  # Arrange the buttons in a 2x8 grid
    cells.append(cell)

# Create the buttons
submitButton = tk.Button(frame, text="Generate", command=genQR, bg="green", fg="white", font=font)
closeButton = tk.Button(frame, text="Close", command=close_window, bg="red", fg="white", font=font)
refreshButton = tk.Button(frame, text="Refresh", command=refresh, bg="blue", fg="white", font=font)

# Create the labels
builder_label = tk.Label(frame, text="Builder", font=("Arial", 16))
model_label = tk.Label(frame, text="Model", font=("Arial", 16))
supplier_label = tk.Label(frame, text="Supplier", font=("Arial", 16))
capacity_label = tk.Label(frame, text="Capacity", font=("Arial", 16))
job_label = tk.Label(frame, text="Job reference", font=("Arial", 16))
neey_label = tk.Label(frame, text="NEEY", font=("Arial", 16))

# Place the labels with relative size and position
builder_label.place(relx=dropdownShift, rely=0.05, anchor=tk.E)
model_label.place(relx=dropdownShift, rely=0.2, anchor=tk.E)
supplier_label.place(relx=dropdownShift, rely=0.35, anchor=tk.E)
capacity_label.place(relx=dropdownShift, rely=0.5, anchor=tk.E)
job_label.place(relx=dropdownShift+0.25, rely=0.05, anchor=tk.E)
neey_label.place(relx=dropdownShift+0.25, rely=0.2, anchor=tk.E)

# Create the dropdown menus
builder = ttk.Combobox(frame, values=["Matt", "George", "Craig", "Adaire", "Paul"], font=("Arial", 16))
model = ttk.Combobox(frame, values=["280L (White)", "280 (Black)"], font=("Arial", 16))
supplier = ttk.Combobox(frame, values=["Fogstar", "Ecobat", "Other (type here)"], font=("Arial", 16))
capacity = ttk.Combobox(frame, values=["280Ah", "304Ah", "Other (type here)"], font=("Arial", 16))
job = tk.Entry(frame, font=("Arial", 16))
neey = ttk.Combobox(frame, values=["Yes", "No"], font=("Arial", 16))

# Place the dropdown menus with relative size and position
builder.place(relx=dropdownShift, rely=0.125, relwidth=0.1, relheight=0.1, anchor=tk.E)
model.place(relx=dropdownShift, rely=0.275, relwidth=0.1, relheight=0.1, anchor=tk.E)
supplier.place(relx=dropdownShift, rely=0.425, relwidth=0.1, relheight=0.1, anchor=tk.E)
capacity.place(relx=dropdownShift, rely=0.575, relwidth=0.1, relheight=0.1, anchor=tk.E)
job.place(relx=dropdownShift+0.25, rely=0.125, relwidth=0.1, relheight=0.1, anchor=tk.E)
neey.place(relx=dropdownShift+0.25, rely=0.275, relwidth=0.1, relheight=0.1, anchor=tk.E)

# Move the buttons to the bottom of the window
submitButton.place(relx=0.1, rely=bigButtonHeight, relwidth=0.2, relheight=0.1, anchor=tk.W)
closeButton.place(relx=0.6, rely=bigButtonHeight, relwidth=0.2, relheight=0.1, anchor=tk.W)
refreshButton.place(relx=0.35, rely=bigButtonHeight, relwidth=0.2, relheight=0.1, anchor=tk.W)

# Start the event loop
window.mainloop()