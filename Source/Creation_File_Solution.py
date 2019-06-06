import sys

def write_solution(name_of_instance, nodes_to_evacuate, nature_of_solution, value_of_aim_function, processing_time, method, free_space = ""): #format for creating a solution file 
    nmb_of_nodes_to_evacuate = 0
    for k in nodes_to_evacuate:
        nmb_of_nodes_to_evacuate += 1
    f = open("../Solutions/SupDates/" + name_of_instance, "w")

    f.write(name_of_instance + "\n")
    f.write(str(nmb_of_nodes_to_evacuate) + "\n")
    for id, values  in nodes_to_evacuate.items():
    
        f.write(str(id) + " " + str(values[0]) + " " + str(values[1]) + "\n")
    f.write(nature_of_solution + "\n")
    f.write(str(value_of_aim_function) + "\n")
    f.write(str(processing_time) + "\n")
    f.write(method + "\n")
    f.write(free_space + "\n")

    f.close()
