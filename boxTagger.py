import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import random
import segno
import os
from PIL import Image, ImageDraw, ImageFont

conn = sqlite3.connect("serial_numbers.db")
c = conn.cursor()

# -----------------Tables-----------------#

c.execute(
    """
    CREATE TABLE IF NOT EXISTS serial_numbers (
        serial_number TEXT PRIMARY KEY,
        Builder TEXT,
        Build_Date TEXT,
        Model TEXT,
        Supplier TEXT,
        Capacity TEXT,
        Job TEXT,
        Neey TEXT
    )
"""
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS cell_serial_numbers (
        cell_serial_number TEXT PRIMARY KEY,
        assigned_battery TEXT,
        cell_position TEXT
    )
"""
)

# -----------------Functions-----------------#


def check_serial_exists(serial_number):
    c.execute("SELECT * FROM serial_numbers WHERE serial_number = ?", (serial_number,))
    return c.fetchone() is not None


def generate_new_serial_number():
    number = random.randint(0, 99999999)
    serial = "OGP00" + str(number).zfill(8)
    return serial


def generate_serial_number():
    while True:
        serial_number = generate_new_serial_number()
        print(serial_number)
        if not check_serial_exists(serial_number):
            serial_number_entry.delete(0, "end")
            serial_number_entry.insert(0, serial_number)
            refresh_image()
            return serial_number


def save_to_database():
    refresh_image()
    serial_number = serial_number_entry.get()
    Builder = Builder_entry.get()
    Build_Date = Build_Date_entry.get()
    Model = Model_entry.get()
    Supplier = Supplier_entry.get()
    Capacity = Capacity_entry.get()
    Job = Job_entry.get()
    Neey = Neey_entry.get()
    c.execute(
        "INSERT OR REPLACE INTO serial_numbers (serial_number, Builder, Build_Date, Model, Supplier, Capacity, Job, Neey) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (serial_number, Builder, Build_Date, Model, Supplier, Capacity, Job, Neey),
    )
    conn.commit()


def display_properties(serial_number):
    c.execute(
        "SELECT Builder, Build_Date, Model, Supplier, Capacity, Job, Neey FROM serial_numbers WHERE serial_number = ?",
        (serial_number,),
    )
    row = c.fetchone()
    refresh_image()
    if row is not None:
        Builder, Build_Date, Model, Supplier, Capacity, Job, Neey = row
        Builder_entry.delete(0, "end")
        Builder_entry.insert(0, Builder)
        Build_Date_entry.delete(0, "end")
        Build_Date_entry.insert(0, Build_Date)
        Model_entry.delete(0, "end")
        Model_entry.insert(0, Model)
        Supplier_entry.delete(0, "end")
        Supplier_entry.insert(0, Supplier)
        Capacity_entry.delete(0, "end")
        Capacity_entry.insert(0, Capacity)
        Job_entry.delete(0, "end")
        Job_entry.insert(0, Job)
        Neey_entry.delete(0, "end")
        Neey_entry.insert(0, Neey)

    c.execute(
        "SELECT assigned_battery, cell_position FROM cell_serial_numbers WHERE cell_serial_number = ?",
        (serial_number,),
    )
    rows = c.fetchall()
    if rows is not None:
        for row in rows:
            assigned_battery, cell_position = row
            # Assuming you have a dictionary that maps cell positions to grid elements
            grid_element = cell_position_to_grid_element[cell_position]
            grid_element.delete(0, "end")
            grid_element.insert(0, assigned_battery)
            print(assigned_battery, cell_position)


def genQRCode(serial):
    qrcode = segno.make_qr(str(serial))
    qrcode.save(
        "images/current.png",
        scale=10,
        border=2,
    )


def genQR(serial):
    save_to_database()
    textTop = "OGP"
    textBottom = serial

    genQRCode(serial)
    refresh_image()

    img = Image.open("images/current.png")
    bg = Image.new("RGB", (580, 290), (255, 255, 255))

    bg.paste(img, (0, 0))
    bg.save("images/combined.png")
    bg = Image.open("images/combined.png")

    draw = ImageDraw.Draw(bg)
    fontTop = ImageFont.truetype("arial.ttf", 122)
    fontBottom = ImageFont.truetype("arial.ttf", 30)

    draw.text((275, 75), textTop, fill="black", font=fontTop)
    draw.text((25, 250), textBottom, fill="black", font=fontBottom)

    bg.save(f"images/{serial}.png")


def batchQR(Repeat):
    for i in range(int(Repeat)):
        genQR(generate_serial_number())


def refresh_image():
    genQRCode(serial_number_entry.get())
    new_image = tk.PhotoImage(file="images/current.png")
    image_label.configure(image=new_image)
    image_label.image = new_image


# -----------------GUI-----------------#

root = tk.Tk()
frame = tk.Frame(root)
frame.grid()


outer_frame = tk.Frame(root, width=1200, height=500)
outer_frame.place(relx=0.5, rely=0.5, anchor="center")

input_frame = tk.Frame(root)
button_frame = tk.Frame(root)
cell_frame = tk.Frame(root)

frame.place(in_=outer_frame, anchor="c", relx=0.5, rely=0.5)
input_frame.place(in_=outer_frame, anchor="e", relx=0.3, rely=0.5)
button_frame.place(in_=outer_frame, anchor="center", relx=0.5, rely=0.5)
cell_frame.place(in_=outer_frame, anchor="w", relx=0.7, rely=0.5)


root.geometry("1200x500")

# -----------------Inputs-----------------#

serial_number_label = tk.Label(input_frame, text="Serial Number:").pack()
serial_number_entry = tk.Entry(input_frame)
serial_number_entry.pack()

Builder_label = tk.Label(input_frame, text="Builder:").pack()
Builder_entry = tk.Entry(input_frame)
Builder_entry.pack()

Build_Date_label = tk.Label(input_frame, text="Build Date:").pack()
Build_Date_entry = tk.Entry(input_frame)
Build_Date_entry.pack()

Model_label = tk.Label(input_frame, text="Model:").pack()
Model_entry = tk.Entry(input_frame)
Model_entry.pack()

Supplier_label = tk.Label(input_frame, text="Supplier:").pack()
Supplier_entry = tk.Entry(input_frame)
Supplier_entry.pack()

Capacity_label = tk.Label(input_frame, text="Capacity:").pack()
Capacity_entry = tk.Entry(input_frame)
Capacity_entry.pack()

Job_label = tk.Label(input_frame, text="Job:").pack()
Job_entry = tk.Entry(input_frame)
Job_entry.pack()

Neey_label = tk.Label(input_frame, text="Neey:").pack()
Neey_entry = tk.Entry(input_frame)
Neey_entry.pack()

generate_button = tk.Button(
    button_frame, text="Generate Serial Number", command=generate_serial_number
)
generate_button.pack(padx=10, pady=10)

save_button = tk.Button(button_frame, text="Save to Database", command=save_to_database)
save_button.pack(padx=10, pady=10)

refresh_button = tk.Button(
    button_frame,
    text="Refresh Properties",
    command=lambda: display_properties(serial_number_entry.get()),
)
refresh_button.pack(padx=10, pady=10)

generate_qr_button = tk.Button(
    button_frame,
    text="Generate QR Code",
    command=lambda: genQR(serial_number_entry.get()),
)
generate_qr_button.pack(padx=10, pady=10)

generate_qr_button_batch = tk.Button(
    button_frame,
    text="Generate Batch QR Code",
    command=lambda: batchQR(Repeat_entry.get()),
)
generate_qr_button_batch.pack(padx=10, pady=10)

image = tk.PhotoImage(file="images/current.png")
image_label = tk.Label(root, image=image)
image_label.pack()

# -----------------Cell Serials-----------------#

cell_position_to_grid_element = {}

for i in range(1, 9):
    cell_position_to_grid_element[f"Cell {i}"] = tk.Entry(cell_frame)
    cell_position_to_grid_element[f"Cell {i}"].grid(row=i - 1, column=3)
    cell_position_to_grid_element[f"Cell {i}"].insert(0, f"Cell {i}")

for i in range(9, 17):
    cell_position_to_grid_element[f"Cell {i}"] = tk.Entry(cell_frame)
    cell_position_to_grid_element[f"Cell {i}"].grid(row=i - 9, column=4)
    cell_position_to_grid_element[f"Cell {i}"].insert(0, f"Cell {i}")


def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))


root.bind("<F11>", toggle_fullscreen)
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
conn.close()
