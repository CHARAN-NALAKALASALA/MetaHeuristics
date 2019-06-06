import sys
import time
import Read_data as read
import Verification_Solution as VeSo
import Creation_file_Solution as CfSo

def Calculation_Inferior_Bound(evac_nodes,arcs,name):
    start_time = time.time()
    params_sol = {} #Creation of solution parameters with rate x of maximum evacuation
    for x, x_value in evac_nodes.items():
        params_sol[x] = (min(x_value['max_rate'],min([arcs[x_arc]['capacity'] for x_arc in x_value['route']])),0)
    gantt_blocs = VeSo.create_blocs(evacuation_nodes,arcs,params_sol)
    inf = VeSo.objective_Calculation(evacuation_nodes,gantt_blocs)
    if VeSo.capacity_verification(evacuation_nodes,arcs,gantt_blocs):
        nature_of_solution = "valid"
    else:
        nature_of_solution = "invalid"
    end_time = time.time()
    fs.write_solution(name, params_sol, nature_of_solution, inf, end_time-start_time, "Inferior Bound")
    return inf

if __name__== "__main__":
    dataname = sys.argv[1]
                                    
    pathfile = "../InstancesInt/"   # pathfile = "../"
    (my_evac,my_graph) = read.read_data(pathfile + dataname)
    print("Inferior Bound:", Calculation_Inferior_Bound(my_evac,my_graph,dataname + "-sol_inf"))
