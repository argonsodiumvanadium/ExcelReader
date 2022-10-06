import pandas as pd
import json
from math import isnan

KEYWORDS = ["BREAKFAST","LUNCH", "SNACK", "DINNER","~~EOF~~"]

"""
loads the excel sheet to a dictionary
"""
def loads (filename='testdoc.xlsx'):
    return reparse(*parse(open_excel(filename)))

"""
opens an excel sheet to give a pandas.DataFrame object

args : 
    string filename 

returns :
    pandas.DataFrame excel
"""
def open_excel (filename='testdoc.xlsx'):
    print(filename)
    excel = pd.read_excel(filename)
    print(excel)
    
    return excel

"""
This is the crude parsing done by me to get the data from
the pandas.DataFrame object into a more malleble format

args :
    pandas.DataFrame sheet

returns:
    string [] days
    dict meal_map

the format of the meal map is
{
    "Breakfast" : [
        ["typeoffood"       ,"B1","B2", "B3" ... "B7"],
        ["anothertypeoffood","B2","B3", "B57" ... "B87"],
    ],

    "Lunch" : [ ... ],

    ...
    
    "Dinner" : [ ... ]
}
"""
def parse(sheet):
    current_value=""
    meal_map = {}

    days = sheet.columns[1:]

    for index, rows in sheet.iterrows():
        row = list(rows)
        value = get_different_meals(row)

        if value[0]:
            current_value = row[0]
            meal_map[current_value] = []
            continue

        meal_map[current_value].append(row)

    return (meal_map,days)

"""
This is basically a parser which gets all the different
meals present and groups them, meals in question being
Breakfast, Lunch etc ..

args:
    _rows : pandas.row object ??
    returns : 
        bool   is_new_meal   # basically if the meal 
                             # is a new item and needs 
                             # to be appended
        string name_of_meal  # name of the new meal if there
                             # is one

the function is volatile, as in it affects other variables
not present in the function

AFFECTS :
    string [] keywords
"""
def get_different_meals (_row):
    global KEYWORDS
    row = list(_row)
    if KEYWORDS[0].upper() in row[0].upper():
        print("hey")
        KEYWORDS = KEYWORDS[1:]
        return True,row[0]

    return False, row[0]

"""
pretty prints a dict, used for debugging
args :
    dict d

"""
def ppdict (d):
    print(json.dumps(d,indent=4))

"""
this function reparses the data into a more malleble form
so that one can use the data with much more ease

args :
    dict meal_map
    string [] days

returns :
    dict final_dict

the format of the dict being returned is
{
    "Breakfast" : {
        "Monday" : {
            "typeoffood1" : "b1",
            "typeoffood2" : "b2",
             ...
        },
        "Tuesday" : {
            "typeoffood1" : "b3",
            "typeoffood2" : "b4".
        }
    }
}
"""
def reparse (meal_map, days):
    final_dict = dict.fromkeys(
            meal_map.keys(),
            dict.fromkeys(days,{})
            )

    for key in meal_map.keys():
        final_dict[key] = {}
        for day in days:
            final_dict[key][day] = {}

    for meal, values in meal_map.items():
        for value in values:
            meal_type = value[0]
            food_items= value[1:]

            for day,food_item in zip(days, food_items):
                print(meal, day, meal_type, food_item)
                final_dict[meal][day][meal_type] = food_item
    
    return final_dict

if __name__ == "__main__":
    final_dict = loads()
    ppdict(final_dict)
