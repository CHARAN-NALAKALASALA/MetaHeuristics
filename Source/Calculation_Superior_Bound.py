import sys
import time
import read_data as read
import Verification_Solution as VeSo
import Creation_file_Solution as CfSo

def Calculation_Superior_Bound(evacuation_nodes,arcs,name):
    start_time = time.time()
    # used_arcs: dict of the arcs used with the list of evacuation nodes that use it
    used_arcs = {};
    for x, x_value in evacuation_nodes.items():
        for x_arc in x_value['route']:
            if x_arc in used_arcs:
                used_arcs[x_arc].append(x)
            else:
                used_arcs[x_arc] = [x]
    params_sol = {} # creation of solution parameters with maximum evacuation rate 
    for x, x_value in evacuation_nodes.items():
       
        rate = min([arcs[arc]['capacity']//len(used_arcs[arc]) for arc in x_value['route']])
        params_sol[x] = (min(rate,evacuation_nodes[x]['max_rate']),0)
        
    gantt_blocs = VeSo.create_blocs(evac_nodes,arcs,params_sol)
    sup = VeSo.objective_Calculation(evacuation_nodes,gantt_blocs)
    if VeSo.capacity_verification(evacuation_nodes,arcs,gantt_blocs):
        nature_of_solution = "valid"
    else:
        nature_of_solution = "invalid"
        print("invalid")
    end_time = time.time()
    fs.write_solution(name, params_sol, nature_of_solution, sup, end_time-start_time, "Superior Bound")
    return sup

def bound_sup_dates(evacuation_nodes,arcs,name):
    start_time = time.time()
    start_date = 0
    params_sol = {}
    for x, x_value in evacuation_nodes.items():
        rate = min([arcs[arc]['capacity'] for arc in x_value['route']])
        params_sol[x] = (min(rate,evacuation_nodes[x]['max_rate']),start_date)
        start_date = sum([arcs[arc]['length'] for arc in x_value['route']]) + (-(-x_value['pop']//rate)) + start_date
    gantt_blocs = VeSo.create_blocs(evacuation_nodes,arcs,params_sol)
    sup = VeSo.objective_Calculation(evacuation_nodes,gantt_blocs)
    if VeSo.capacity_verification(evacuation_nodes,arcs,gantt_blocs):
        nature_of_solution = "valid"
        print("valid")
    else:
        nature_of_solution = "invalid"
        print("invalid")
    end_time = time.time()
    fs.write_solution(name, params_sol, nature_of_solution, sup, end_time-start_time, "Superior Dates Bound",)
    return sup


if __name__== "__main__":
    dataname = sys.argv[1]
   
    pathfile = "../InstancesInt/"  # pathfile = "../"
    (my_evac,my_graph) = read.read_data(pathfile + dataname + ".full")
    
    print("Superior Bound:", Superiordatesbound(my_evac,my_graph,dataname + "-sol_sup"))