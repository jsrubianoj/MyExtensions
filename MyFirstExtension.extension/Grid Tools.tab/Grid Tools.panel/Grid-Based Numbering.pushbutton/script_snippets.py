"""Calculates total volume of all walls in the model."""

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import Selection,TaskDialog
from Autodesk.Revit.Attributes import *
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app=__revit__.Application

# Check if shared parameters file is loaded
shared_parameters_file=app.OpenSharedParameterFile()
if not shared_parameters_file:
    forms.alert('No shared parameters file found')

# Sort all parameters in the shared parameters file
shared_params_dict={}
for group in shared_parameters_file.Groups:
    for param_def in group.Definitions:
        combined_name = '[{}]_{}'.format(group.Name, param_def.Name)
        shared_params_dict[combined_name]=param_def

selected_parameters= forms.SelectFromList.show(sorted(shared_params_dict.keys()), button_name='Select Parameters', multiselect=True)

selected_parameters_definitions=[shared_params_dict[param_name] for param_name in selected_parameters]

# Select categories and create CategorySet
cat_set=app.Create.NewCategorySet()
cat_plumbing_eq=Category.GetCategory(doc, BuiltInCategory.OST_PlumbingFixtures)
cat_walls=Category.GetCategory(doc, BuiltInCategory.OST_Walls)
cat_set.Insert(cat_plumbing_eq)
cat_set.Insert(cat_walls)

# Create a new instance binding
instance_binding=app.Create.NewInstanceBinding(cat_set)

#Select Parameter Group
parameter_group=BuiltInParameterGroup.PG_IDENTITY_DATA

# Add Parameter
t=Transaction(doc, 'Add Shared Parameters')
t.Start()
for param_def in selected_parameters_definitions:
    try:
        doc.ParameterBindings.Insert(param_def, instance_binding, parameter_group)
        print('Parameter {} added successfully'.format(param_def.Name))
    except:
        print('Parameter {} not added'.format(param_def.Name))
t.Commit()    


selected_elements = uidoc.Selection.PickObjects(Selection.ObjectType.Element, 'Select elements to add shared parameters')
# selected_elements_instances = [doc.GetElement(e.ElementId) for e in selected_elements]
if len(selected_elements)==0:
    print(selected_elements)
    TaskDialog.Show('Error','No elements selected')
else:
    print(selected_elements)
    TaskDialog.Show('Info','{} elements selected'.format(len(selected_elements)))

def get_or_create_parameter(doc, param_name):
    """Ensure the shared parameter exists, otherwise create it."""
    param_found = False
    params = doc.FamilyManager.Parameters if doc.IsFamilyDocument else doc.ParameterBindings
    
    for param in params:
        if param.Name == param_name:
            param_found = True
            break
    
    if not param_found:
        with Transaction(doc, "{}Create.format(param_name)") as t:
            t.Start()
            param = doc.FamilyManager.AddParameter(param_name, ParameterType.Text, False) if doc.IsFamilyDocument \
                else doc.AddSharedParameter(param_name, BuiltInCategory.OST_GenericModel)
            t.Commit()
# t = Transaction(doc, "Add Shared Parameters")
# t.Start()

for elem_id in selected_elements:
    elem = doc.GetElement(elem_id)
    elem_type = doc.GetElement(elem.GetTypeId())
    
    param_type_grid_square = elem_type.LookupParameter("Grid Square")
    param_type_numbers = elem_type.LookupParameter("Numbers")
    if param_type_grid_square:
        print("Grid Square parameter found in type")
    else:
        print("Grid Square parameter not found in type")
        get_or_create_parameter(doc, "Grid Square")
        get_or_create_parameter(doc, "Number")    
        
# t.Commit()

# Creating collector instance and collecting all the grids from the model
grid_collector = FilteredElementCollector(doc)\
                   .OfCategory(BuiltInCategory.OST_Grids)\
                   .WhereElementIsNotElementType()

vertical_grids=[]
horizontal_grids=[]
for grid in grid_collector:
    if round(grid.GetExtents().MaximumPoint.X,8) == round(grid.GetExtents().MinimumPoint.X,8):
        vertical_grids.append(grid)
    else:
        horizontal_grids.append(grid)




















#Copyright (c) mostafa el ayoubi
# #Data-Shapes www.data-shapes.net 2016 elayoub.mostafa@gmail.com


# import clr
# import System
# clr.AddReference('RevitAPI')
# from Autodesk.Revit.DB import*
# clr.AddReference('RevitServices')
# from RevitServices.Persistence import DocumentManager
# from RevitServices.Transactions import TransactionManager
# clr.AddReference('RevitAPIUI')
# from Autodesk.Revit.UI import *
# from Autodesk.Revit import Creation

# doc = DocumentManager.Instance.CurrentDBDocument
# uidoc = DocumentManager.Instance.CurrentUIDocument
# app = doc.Application

# def AddShared(cat, para, gr, ins):

# 	if isinstance(cat, list):
# 		category = UnwrapElement([i for i in cat])
# 	else:
# 		category= UnwrapElement([cat])
		
# 	#creating category set
# 	catset = app.Create.NewCategorySet()
# 	[catset.Insert(j) for j in category]
	
# 	if isinstance(para, list):
# 		parameters = [i for i in para]
# 	else:
# 		parameters = [para]
		
# 	try:
# 		group = [a for a in System.Enum.GetValues(BuiltInParameterGroup) if a == gr][0]
# 	except:
# 		group = [a for a in System.Enum.GetValues(BuiltInParameterGroup) if str(a) == gr][0]
# 	i = 0
	
# 	TransactionManager.Instance.EnsureInTransaction(doc)
	
# 	#Determining whether the parameters are type or instance
# 	if ins:
# 		bind = app.Create.NewInstanceBinding(catset)
# 	else : 
# 		bind = app.Create.NewTypeBinding(catset)
# 	#Adding the parameters to the project
# 	bindmap = doc.ParameterBindings
# 	try:
# 		bindmap.Insert(para, bind, group)
# 		i += 1
# 		a = "Exitoso"
# 	except:
# 		a = "Falla"

# 	TransactionManager.Instance.TransactionTaskDone()
# 	return a
	
# categories = IN[0]
# parameters = IN[1]
# group = IN[2]
# instance = IN[3]
# count = 0
# res =[]
# for count in range(len(parameters)):
# 	res.append(AddShared(categories[count],parameters[count],group,instance[count]))
# OUT = res


from pyrevit import forms, script, revit
from pyrevit.revit import Transaction
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ParameterType, UnitType, XYZ, Grid

def get_or_create_parameter(doc, param_name):
    """Ensure the shared parameter exists, otherwise create it."""
    param_found = False
    params = doc.FamilyManager.Parameters if doc.IsFamilyDocument else doc.ParameterBindings
    
    for param in params:
        if param.Definition.Name == param_name:
            param_found = True
            break
    
    if not param_found:
        with Transaction(doc, f"Create {param_name}") as t:
            t.Start()
            param = doc.FamilyManager.AddParameter(param_name, ParameterType.Text, False) if doc.IsFamilyDocument \
                else doc.AddSharedParameter(param_name, BuiltInCategory.OST_GenericModel)
            t.Commit()

def find_closest_grid_square(grids, element_location):
    """Determine the closest grid intersection."""
    closest_vertical, closest_horizontal = None, None
    min_v_dist, min_h_dist = float('inf'), float('inf')
    
    for grid in grids:
        if grid.Curve:
            closest_point = grid.Curve.Project(element_location).XYZPoint
            dist = element_location.DistanceTo(closest_point)
            
            if grid.IsCurved:
                continue
            
            if abs(grid.Curve.Direction.X) > abs(grid.Curve.Direction.Y):
                if dist < min_h_dist:
                    min_h_dist = dist
                    closest_horizontal = grid.Name
            else:
                if dist < min_v_dist:
                    min_v_dist = dist
                    closest_vertical = grid.Name
    
    return f"{closest_vertical}-{closest_horizontal}" if closest_vertical and closest_horizontal else "Unknown"

def get_sorted_elements_by_proximity(elements, start_element):
    """Sort elements by distance from the user-selected starting element."""
    start_location = start_element.Location.Point
    return sorted(elements, key=lambda e: start_location.DistanceTo(e.Location.Point))

def main():
    doc = revit.doc
    uidoc = revit.uidoc
    grids = FilteredElementCollector(doc).OfClass(Grid).ToElements()
    elements = uidoc.Selection.PickObjects(forms.Selection.pick_elements, "Select elements to number")
    selected_elements = [doc.GetElement(e.ElementId) for e in elements]
    
    if not selected_elements:
        forms.alert("No elements selected.", exitscript=True)
    
    start_ref = uidoc.Selection.PickObject(forms.Selection.pick_element, "Pick starting element for numbering")
    start_element = doc.GetElement(start_ref.ElementId)
    sorted_elements = get_sorted_elements_by_proximity(selected_elements, start_element)
    
    get_or_create_parameter(doc, "Grid Square")
    get_or_create_parameter(doc, "Number")
    
    with Transaction(doc, "Assign Grid Square and Number") as t:
        t.Start()
        for index, element in enumerate(sorted_elements, start=1):
            location = element.Location.Point
            grid_square = find_closest_grid_square(grids, location)
            element.LookupParameter("Grid Square").Set(grid_square)
            element.LookupParameter("Number").Set(str(index))
        t.Commit()
    
    forms.alert("Grid-Based Numbering Completed.")

if __name__ == "__main__":
    main()
