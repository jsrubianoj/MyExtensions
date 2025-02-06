from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import Selection,TaskDialog,TaskDialogCommonButtons
from Autodesk.Revit.Attributes import *
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app=__revit__.Application
revit_version=int(app.VersionNumber)

# Function to set the grid square value
def get_closest_grids(elem_id):
    closest_vertical_grid, closest_horizontal_grid = None,None
    closest_vertical_distance, closest_horizontal_distance  = float('inf'),float('inf')

    # Loop through all the vertical grids to find the closest one
    for vert_grid in vertical_grids:
        distance_x = abs(elem_id.Location.Point.X-vert_grid.GetExtents().MinimumPoint.X)
        if distance_x < closest_vertical_distance:
            closest_vertical_distance = distance_x
            closest_vertical_grid = vert_grid

    # Loop through all the horizontal grids to find the closest one
    for horizontal_grid in horizontal_grids:
        distance_y = abs(elem_id.Location.Point.Y-horizontal_grid.GetExtents().MinimumPoint.Y)
        if distance_y < closest_horizontal_distance:
            closest_horizontal_distance = distance_y
            closest_horizontal_grid = horizontal_grid
    grid_square_value=str(closest_vertical_grid.Name)+"-"+str(closest_horizontal_grid.Name)
    return grid_square_value

def get_sorted_elements_by_proximity(elements, start_element):
    # Get the location point of the start element
    start_location = doc.GetElement(start_element).Location.Point

    # Define a helper function to compute the distance of an element from the start location
    def get_distance(element):
        return start_location.DistanceTo(element.Location.Point)

    # Sort elements using the computed distance
    elements = [doc.GetElement(e) for e in elements]
    sorted_elements = sorted(elements, key=get_distance)
    return sorted_elements



# Select Elements to update their parameters
TaskDialog.Show("Element Selection","Select Elements to update their Grid Square and Number parameters",TaskDialogCommonButtons.Ok)
selected_elements = uidoc.Selection.PickObjects(Selection.ObjectType.Element, 'Select elements to add shared parameters')

# Select starting element
TaskDialog.Show("First Element","Select the first element",TaskDialogCommonButtons.Ok)
first_element = uidoc.Selection.PickObject(Selection.ObjectType.Element, 'Select the starting element')

# Search for Parameters txt file
shared_parameters_file=app.OpenSharedParameterFile()
if not shared_parameters_file:
    forms.alert('No shared parameters file found')

shared_params_dict={}
for group in shared_parameters_file.Groups:
    for param_def in group.Definitions:
        combined_name = '[{}]_{}'.format(group.Name, param_def.Name)
        shared_params_dict[combined_name]=param_def
selected_parameters_definitions=shared_params_dict.values()

# Get selected elements categories
if revit_version >= 2023:
    category_to_use=BuiltInCategory.OST_PlumbingEquipment
else:
    category_to_use=BuiltInCategory.OST_PlumbingFixtures


# Select categories and create CategorySet
cat_set=app.Create.NewCategorySet()
cat_plumbing_fix=Category.GetCategory(doc, category_to_use)
cat_set.Insert(cat_plumbing_fix)

# Create a new instance binding
instance_binding=app.Create.NewInstanceBinding(cat_set)
# InstanceBinding(cat_set)

#Select Parameter Group
if revit_version >= 2024:
    parameter_group=GroupTypeId.General
else:
    parameter_group=BuiltInParameterGroup.PG_GENERAL

# Add Shared Parameters
t=Transaction(doc, 'Add Shared Parameters')
t.Start()
for param_def in selected_parameters_definitions:
    doc.ParameterBindings.Insert(param_def, instance_binding, parameter_group)
t.Commit()    


# Get type ids of selected elements
for elem_id in selected_elements:
    elem = doc.GetElement(elem_id)
    elem_type = doc.GetElement(elem.GetTypeId())
    param_type_grid_square = elem.LookupParameter("Grid Square")
    param_type_numbers = elem.LookupParameter("Number")

# Creating collector instance and collecting all the grids from the model
grid_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType()

# Dividing the grids into vertical and horizontal grids
vertical_grids=[]
horizontal_grids=[]
for grid in grid_collector:
    if round(grid.GetExtents().MaximumPoint.X,5) == round(grid.GetExtents().MinimumPoint.X,5):
        vertical_grids.append(grid)
    else:
        horizontal_grids.append(grid)


t=Transaction(doc, 'Set Grid Square and Number Parameters')
t.Start()
for elem_id in selected_elements:
    elem = doc.GetElement(elem_id)
    param_type_grid_square = elem.LookupParameter("Grid Square")
    param_type_grid_square.Set(get_closest_grids(elem))
    param_type_numbers = elem.LookupParameter("Numbers")
t.Commit()


sorted_elements=get_sorted_elements_by_proximity(selected_elements, first_element)
t=Transaction(doc, 'Set Number Parameters')
t.Start()
for elem in sorted_elements:
    elem.LookupParameter("Number").Set(sorted_elements.index(elem)+1)
t.Commit()


TaskDialog.Show("Completed","Elements updated successfully",TaskDialogCommonButtons.Ok)
