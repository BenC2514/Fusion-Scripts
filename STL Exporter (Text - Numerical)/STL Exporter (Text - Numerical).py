#Author- BenC2514
#Description- Bulk export STL's with variation on numerical text. Make sure sketch is in tree root

# Import necessary modules
import adsk.core, adsk.fusion, adsk.cam, traceback, tkinter as tk
from tkinter import filedialog, messagebox

# Submit function to handle form submission
def submit():
    # Get input values from the form
    sketch_name = sketch_name_entry.get()
    min_num = min_num_entry.get()
    max_num = max_num_entry.get()
    folder_path = folder_path_entry.get()
    
    # Validate inputs
    if not all((sketch_name, min_num, max_num, folder_path)):
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    try:
        min_num = int(min_num)
        max_num = int(max_num)
        if min_num >= max_num:
            raise ValueError("Minimum number must be less than maximum number.")
    except ValueError:
        messagebox.showerror("Error", "Min & Max number should be an integar.")
        return
    
    # Close the Tkinter window
    root.destroy()
    
    # Call the Fusion 360 script function with the input values
    run_export(sketch_name, min_num, max_num, folder_path)

# Browse folder function to handle selecting folder path
def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

# Clear fields function to clear all form fields
def clear_fields():
    sketch_name_entry.delete(0, tk.END)
    min_num_entry.delete(0, tk.END)
    max_num_entry.delete(0, tk.END)
    folder_path_entry.delete(0, tk.END)

# Function to bulk export STLs with variation on numerical text
def run_export(sketch_name, min_num, max_num, folder_path):
    debug = False
    ui = None    
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComponent = design.rootComponent
        exportMgr = design.exportManager
        sketches = rootComponent.sketches
        
        # Create list of ascending numbers up to max limit
        groups = list(range(int(min_num), int(max_num)+1, 1))
        
        # Must match sketch name in Document Sketches
        textSketch = sketches.itemByName(str(sketch_name))
       
        for x in groups:
            app.log("changing to " + str(x))

            # Change the sketch text and majorAxis User Parameter
            try:
                textSketch.sketchTexts[0].text = str(x)
            except AttributeError:
                messagebox.showerror("Error", "Could not find text sketch in project.\nCheck sketch is in root component.")
                exit()

            # Repaint to see the body update
            design.computeAll()
            app.activeViewport.refresh()
            
            # Create export options
            exportFile = f"{folder_path}/{rootComponent.name}_{x}"
            stlExportOptions = exportMgr.createSTLExportOptions(rootComponent, exportFile)
            stlExportOptions.sendToPrintUtility = False
            
            # Export STL file
            app.log("exporting " + str(x))
            exportMgr.execute(stlExportOptions)
            app.log("done exporting " + str(x))

        ui.messageBox('Finished.')
    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:\n{traceback.format_exc()}')

# Create main window
root = tk.Tk()
root.title("Sketch Info")

# Set window dimensions and position
window_width = 400
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Configure window background color
root.configure(background="#F0F0F0")

# Frame for labels and entries
frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(pady=10)

# Labels
labels = ["Sketch Name:", "Min Number:", "Max Number:", "Folder Path:"]
for i, label_text in enumerate(labels):
    tk.Label(frame, text=label_text, bg="#F0F0F0").grid(row=i, column=0, padx=5, pady=5, sticky="e")

# Entries
entries = [tk.Entry(frame) for _ in range(len(labels))]
for i, entry in enumerate(entries):
    entry.grid(row=i, column=1, padx=5, pady=5)
    
sketch_name_entry, min_num_entry, max_num_entry, folder_path_entry = entries

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
