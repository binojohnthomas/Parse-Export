#wrapper class to get data of all app - looping through
import os
f = open("ParseAppList.csv")
applist = f.readlines()

for app in applist:

    arg_list = (app.split(','))
    #print(app)
    #print arg_list[]

    python_exe = "python parse_export_data.py "+arg_list[0]+" "+arg_list[1]+" "+arg_list[2]+" "+arg_list[3]
    print python_exe
    os.system(python_exe)


#os.system("python2 parse_export_data.py asvTestBible3 wLlFWQ80bIy4W4VJafAHaZeusiUrCR87ODMOVVVz vU4fAv2FBneosBpCXGr1SAnQCUfUDHm9l99YZual TaTBfU0XYgnRgO3XNCAECi1kEVsKqEfKFGcXkPbx")