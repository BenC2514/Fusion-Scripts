#Author- BenC2514
#Description- Bulk export STL's with variation on numerical text. Make sure sketch is tree root

import adsk.core, adsk.fusion, adsk.cam, traceback

debug = False

def run(context):

    ui = None
    
    try:
  
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComponent = design.rootComponent
        exportMgr = design.exportManager
        sketches = rootComponent.sketches

        #User inputs for SketchName, MaxNum, FilePath
        defaultSketchName = 'text'
        SketchName = ui.inputBox('Name of the Sketch to be changes: ', 
                                'Sketch Name', defaultSketchName)[0]
        
        defaultGroupNumMax = '10'
        GroupNumMax_Input = ui.inputBox('Input Max Num: ', 
                                'Define Max Num.', defaultGroupNumMax)[0]
        
        #create list of ascending number up to max limit
        groups = list(range(1,int(GroupNumMax_Input)+1,1))
        
        if debug == True:
            exportPath = ("C:\\Users\\u4125590\Downloads\\test")
        else:
            defaultInputFolder = 'C:\\'
            exportPath = ui.inputBox('Input path to save folder: ', 
            'Define Save Folder', defaultInputFolder)[0]
        
        if debug == True:    
            for sketch in sketches:
                app.log(sketch.name)    
     
        # Must match sketch name in Document Sketches
        textSketch = sketches.itemByName(str(SketchName))
       
        for x in groups:
            
            app.log("changing to " + str(x))
            
            # .sketchTexts returns the sketch text collection
            # Change the sketch text and majorAxis User Parameter
            textSketch.sketchTexts[0].text = str(x)

            
            # Repaint to see the body update
            design.computeAll()
            app.activeViewport.refresh()
            
            # Create export options
            exportFile = exportPath + ("\\") + (rootComponent.name) + ("_") + str(x)
            stlExportOptions = exportMgr.createSTLExportOptions(rootComponent,exportFile)
            stlExportOptions.sendToPrintUtility = False
            
            # Export STL file
            app.log("exporting " + str(x))
            exportMgr.execute(stlExportOptions)
            app.log("done exporting " + str(x))

        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
