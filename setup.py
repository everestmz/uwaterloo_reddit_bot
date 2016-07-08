import os, sys

file_path = os.path.realpath(__file__)
file_path_array = file_path.split("/")
file_path_array.pop()
file_path_array.pop(0)
file_path = ""

for dir in file_path_array:
    file_path += "/" + dir

if file_path not in sys.path:
    print "Adding " + file_path + " to PYTHONPATH"
    sys.path.append(file_path)

