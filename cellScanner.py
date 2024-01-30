import tkinter as tk
import sqlite3

conn = sqlite3.connect("serial_numbers.db")
c = conn.cursor()


def write_to_database():
    cell_serial_number = cell_serial_entry.get()
    assigned_battery = assigned_battery_entry.get()
    cell_position = cell_position_entry.get()
    # Insert the serial number into the table
    c.execute(
        "INSERT OR REPLACE INTO cell_serial_numbers (cell_serial_number, assigned_battery, cell_position) VALUES (?, ?, ?)",
        (cell_serial_number, assigned_battery, cell_position),
    )

    # Commit the changes and close the connection
    conn.commit()

    # Clear the cell_serial_entry field
    cell_serial_entry.delete(0, tk.END)
    if cell_position_entry.get() == int or cell_position_entry.get() == float:
        cell_position_entry.delete(0, tk.END)
        cell_position_entry.insert(0, int(cell_position) + 1)
        if int(cell_position) > 15:
            cell_position_entry.delete(0, tk.END)
            cell_position_entry.insert(0, 1)
    


# Create the Tkinter window
window = tk.Tk()
window.title("Serial Number Writer")
window.geometry("200x200")

cell_serial_label = tk.Label(window, text="Cell Serial Number:")
cell_serial_label.pack()
cell_serial_entry = tk.Entry(window)
cell_serial_entry.pack()
assigned_battery_label = tk.Label(window, text="Assigned Battery:")
assigned_battery_label.pack()
assigned_battery_entry = tk.Entry(window)
assigned_battery_entry.pack()
cell_position_label = tk.Label(window, text="Cell Position:")
cell_position_label.pack()
cell_position_entry = tk.Entry(window)
cell_position_entry.pack()
cell_position_entry.insert(0, 1)

# Create the button
button = tk.Button(window, text="Write to Database", command=write_to_database)
button.pack()

# Start the Tkinter event loop
window.mainloop()
conn.close()
