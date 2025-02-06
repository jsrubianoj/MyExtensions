# Grid-Based Numbering Tool for pyRevit

## Overview
The **Grid-Based Numbering Tool** is a pyRevit extension that automates the numbering of elements based on their position and assigns a parameter with the grid location of the element. This tool enhances model organization and ensures consistent data handling across projects.

## Features
- Adds a **"Grid Tools"** tab in pyRevit with a button labeled **"Grid-Based Numbering"**.
- Verifies if the parameters **"Grid Square"** and **"Number"** exist in the model, and creates them if they do not.
- Assigns the **Grid Square** parameter to elements based on their closest grid intersection in the format `{Vertical Grid}-{Horizontal Grid}`.
- Assigns the **Number** parameter to elements sequentially based on spatial proximity, starting from a user-selected element.
- Provides a user-friendly interface to select elements and define a starting element interactively.
- Supports Revit versions **2019-2024**.

## Installation
1. Clone or download the repository.
2. Copy the extension folder to your pyRevit extensions directory. You could also save it in a folder of your preference and add it manually to pyRevit using its Settings. See the ['Adding Extensions Manually'](https://pyrevitlabs.notion.site/Install-Extensions-0753ab78c0ce46149f962acc50892491#:~:text=Adding%20Extension%20Manually). in the pyRevit documentation:
   ```sh
   %APPDATA%\pyRevit\Extensions\
   ```
3. Restart Revit and ensure pyRevit is loaded.
4. Navigate to the **"Grid Tools"** tab and use the **"Grid-Based Numbering"** tool.

## Repository Structure
```
|-- MyExtensions/
    |-- Grid Tools.extension/  # pyRevit extension folder
        |-- Grid Tools.tab/  # pyRevit tab folder
            |-- Grid Tools.panel  # pyRevit panel folder
    |-- Testing Models.zip  # Revit testing models
    |-- parameters.txt  # Shared parameters file
    |-- README.md  # This file
```

## Usage
1. Open a Revit model with grids.
2. Click **"Grid-Based Numbering"** under the **"Grid Tools"** tab.
3. Select elements to be modified.
4. Select a starting element interactively.
5. The tool will assign **Grid Square** and **Number** values to the selected elements based on their grid location and spatial order.

## Requirements
- Revit 2019-2024
- [pyRevit](https://pyrevitlabs.notion.site/pyRevit-bd907d6292ed4ce997c46e84b6ef67a0) installed and configured
- A model containing grids and elements (provioded in the zip file)

## Shared Parameters
The `parameters.txt` file in this repository includes the shared parameters that need to be added to the Revit model. Ensure that these parameters are loaded into your project for the tool to function correctly. See [Autodesk Revit Official Documentation](https://help.autodesk.com/view/RVT/2021/ENU/?guid=GUID-94EA2B8E-2C00-4D29-8D5A-C7C6664DE9CE) for more information

## Notes
- The tool is designed to work with any Revit model that includes grids. **The tool works with Plumbing Equipments but could be modified in the future to match any family instance needed**
- If no shared parameters file is detected, the tool will prompt the user with an error message.
- Users are expected to create their own test models for validation.

## License
This project is licensed under the MIT License.

## Contact
For issues or feature requests, please submit a ticket in the repository's issue tracker.

