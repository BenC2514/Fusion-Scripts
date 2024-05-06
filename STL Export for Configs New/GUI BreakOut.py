import tkinter as tk
from tkinter import filedialog, messagebox

def submit():
    sketch_name = sketch_name_entry.get()
    min_num = min_num_entry.get()
    max_num = max_num_entry.get()
    folder_path = folder_path_entry.get()

    # Validate inputs
    if not sketch_name or not min_num or not max_num or not folder_path:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    try:
        min_num = int(min_num)
        max_num = int(max_num)
    except ValueError:
        messagebox.showerror("Error", "Minimum and maximum numbers must be integers.")
        return

    if min_num >= max_num:
        messagebox.showerror("Error", "Minimum number must be less than maximum number.")
        return

    # Do something with the inputs, like printing them
    print("Sketch Name:", sketch_name)
    print("Minimum Number:", min_num)
    print("Maximum Number:", max_num)
    print("Folder Path:", folder_path)

    root.destroy()   

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

def clear_fields():
    sketch_name_entry.delete(0, tk.END)
    min_num_entry.delete(0, tk.END)
    max_num_entry.delete(0, tk.END)
    folder_path_entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Sketch Info")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window width and height
window_width = 400
window_height = 250

# Calculate the position for the window
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and place widgets with colors
root.configure(background="#F0F0F0")

# Frame for labels and entries
frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(pady=10)

# Labels
tk.Label(frame, text="Sketch Name:", bg="#F0F0F0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Label(frame, text="Min Number:", bg="#F0F0F0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Label(frame, text="Max Number:", bg="#F0F0F0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
tk.Label(frame, text="Folder Path:", bg="#F0F0F0").grid(row=3, column=0, padx=5, pady=5, sticky="e")

# Entries
sketch_name_entry = tk.Entry(frame)
sketch_name_entry.grid(row=0, column=1, padx=5, pady=5)
min_num_entry = tk.Entry(frame)
min_num_entry.grid(row=1, column=1, padx=5, pady=5)
max_num_entry = tk.Entry(frame)
max_num_entry.grid(row=2, column=1, padx=5, pady=5)
folder_path_entry = tk.Entry(frame)
folder_path_entry.grid(row=3, column=1, padx=5, pady=5)

# Browse button
browse_button = tk.Button(frame, text="Browse", command=browse_folder, bg="#90EE90")
browse_button.grid(row=3, column=2, padx=5, pady=5)

# Submit and Clear buttons
submit_button = tk.Button(root, text="Submit", command=submit, bg="#ADD8E6")
submit_button.pack(pady=5)
clear_button = tk.Button(root, text="Clear", command=clear_fields, bg="#FFA07A")
clear_button.pack(pady=5)

# Run the main event loop
root.mainloop()

