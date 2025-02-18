import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent

        # Input parameters
        defaultInputMin = '150'
        min_Input = ui.inputBox('Define minimum measurement', "", defaultInputMin)

        defaultInputMax = '200'
        max_Input = ui.inputBox('Define maximum measurement', "", defaultInputMax)

        defaultStep = '10'
        step_Input = ui.inputBox('Input step size', "", defaultStep)

        defaultParam = "length"
        Param_Input = ui.inputBox('Input Parameter Name', "", defaultParam)

        defaultInputFolder = r'C:\Users\u4125590\Downloads\test'
        folderInput = ui.inputBox('Input path to save folder:', "", defaultInputFolder)

        # Create list of sizes from user inputs        
        min_value = float(min_Input[0])
        max_value = float(max_Input[0])
        step_size = float(step_Input[0])
        
        # Generate list of sizes with floating point increments
        sizes = []
        current_size = min_value
        while current_size <= max_value:
            sizes.append(round(current_size, 2))  # Rounding to 2 decimal places for clarity
            current_size += step_size
        
        # Assign parameter to variable & check existance
        ChngeParam = design.allParameters.itemByName(Param_Input[0])
        if ChngeParam is None:
            ui.messageBox(f'Parameter "{Param_Input}" not found.')
            return
        
        # Retrieve the original parameter expression (including its unit)
        origParamExpr = ChngeParam.expression 
        app.log(f'Original value: {origParamExpr}')

        for dim in sizes:
            # Change parameter in project
            ChngeParam.expression = str(dim)

            # Let the view update
            adsk.doEvents()
            
            # Construct the output filename
            filename = f"{folderInput[0]}\\{rootComp.name}_{dim}.stl"

            # Save the file as STL
            exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
            stlOptions = exportMgr.createSTLExportOptions(rootComp)
            stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            stlOptions.filename = filename
            exportMgr.execute(stlOptions)

            app.log("Exported " + str(dim))
    
        # Reset parameter to original value
        ChngeParam.expression = origParamExpr
        adsk.doEvents()

        ui.messageBox('Finished.')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
