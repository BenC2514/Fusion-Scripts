#Author- BenC2514
#Description- Bulk export STL's from CSV file. Make sure sketch is in tree root

# Import necessary modules
import adsk.core, adsk.fusion, adsk.cam, traceback, csv, tkinter as tk
from tkinter import filedialog, messagebox

debug = False

ui = None
try:
    #pull information from fusion project  
    app = adsk.core.Application.get()
    ui  = app.userInterface
    design = adsk.fusion.Design.cast(app.activeProduct)
    rootComponent = design.rootComponent
    exportMgr = design.exportManager
    sketches = rootComponent.sketches
    
    #open csv file from file dialog box
    filename = filedialog.askopenfilename(filetypes=[('CSV','*.csv')])
    file = open(filename, encoding='utf-8-sig')
    #take data as list and close file
    CSVdata = list(csv.reader(file,delimiter=","))    
    file.close
    #collect output path
    userOutputPath = filedialog.askdirectory()
    #user enters text sketch name
    sketch_name = ui.inputBox("Sketch Name")[0]
    # Must match sketch name in Document Sketches
    textSketch = sketches.itemByName(str(sketch_name))
    

    #debugging info
    if debug ==True:
        app.log("User CSV Filename Entry: "+filename)
        app.log("User Output Path Entry: "+userOutputPath)
        app.log("User Text Entry: "+sketch_name)

        app.log("\nCurrent Sketches in project:")
        for sketch in sketches:
            app.log(sketch.name)
    

    for x in CSVdata:
        #loop through CSV data and format
        edtName = str(x).strip("['']")
        app.log("\nExporting: "+ edtName)
        
        try:
            textSketch.sketchTexts[0].text = str(edtName)
        except AttributeError:
            messagebox.showerror("Error", "Could not find text sketch in project.\nCheck sketch is in root component.")
            exit()

        # Compute to see the body update
        design.computeAll()
        app.activeViewport.refresh()


        # Create export options
        fileExport = f"{userOutputPath}/{rootComponent.name}_{edtName}"
        stlExportOptions = exportMgr.createSTLExportOptions(rootComponent, fileExport)
        stlExportOptions.sendToPrintUtility = False

        # Export STL file
        exportMgr.execute(stlExportOptions)


    ui.messageBox('Finished.')
except Exception as e:
    if ui:
        ui.messageBox(f'Failed:\n{traceback.format_exc()}')

