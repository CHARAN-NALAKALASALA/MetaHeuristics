import sys
import Read_data as read

def create_blocs(evacuation_nodes,arcs,solution_info):
    # tuples (departure date, evacuation rate) for all crossed arches
        # solution[(id_node,(node1,node2))] = (start_date,evac_rate)
   
    solution = {}
    for x, x_value in evac_nodes.items():
        (evacuation_rate,start_date) = solution_info[x] 
        for x_arc in x_value['route']:
            solution[(x,x_arc)] = (start_date,evacuation_rate)
            start_date = start_date + arcs[x_arc]['length']
        solution[(x,(x_value['route'][-1][1],'completed'))] = (start_date,evacuation_rate)
    return solution

def objective_Calculation(evacuation_nodes,blocs):
                # in order to attain the complexity O(n)
    obj_x = [(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1])) for x in evacuation_nodes]
    print("objectives: ", obj_x)
    return max(obj_x)

def max_rate_verification(evacuation_nodes,arcs,solution_info):
    for x, x_value in evacuation_nodes.items():
        ok = True
        evacuation_rate = solution_info[x][0]
        #Checking the evacuation rate < Max Evacuation rate 
        if (evacuation_rate <= evacuation_nodes[x]['max_rate']):
            ok = True
            #Checking the evacuation rate < Capacity of traversed arcs
            for x_arc in x_value['route']:
                if evacuation_rate > arcs[x_arc]['capacity']:
                    ok = False
        else:
            ok = False
        return ok

def capacity_verification(evacuation_nodes,arcs,blocs):
    used_arcs = set([tup[1] for tup in blocs if tup[1][1] != 'completed'])
    valid = True
    for a in used_arcs:
        capacity = arcs[a]['capacity']
        sequence = [(blocs[tup][0],blocs[tup][1],-(-evacuation_nodes[tup[0]]['pop']//blocs[tup][1])) for tup in blocs if tup[1] == a]
        start = min(sequence)[0] # starting of traversal 
        end = max([s+d for (s,r,d) in sequence]) #end of traversal
      
        for t in range(start,end):
            number_persons_pers = 0
           
            for (st,rate,ft) in sequence:
                if (t>=st and t<(st+ft)):
                    number_persons = number_persons + rate
           
            if (number_persons>capacity):
    
                valid = False
    return valid

 # Verifies that capacity constraints are proper

def capacity_verification_with_return(evacuation_nodes,arcs,blocs):
    used_arcs = set([tup[1] for tup in blocs if tup[1][1] != 'completed'])

    valid = True
    conflicts = set()
    for a in used_arcs:
        capacity = arcs[a]['capacity']
       
        sequence = [(blocs[tup][0],blocs[tup][1],-(-evacuation_nodes[tup[0]]['pop']//blocs[tup][1])) for tup in blocs if tup[1] == a]
        start = min(sequence)[0] # starting of the passage on arc a
        end = max([s+d for (s,r,d) in sequence]) # end of the passage on arc a
        
        for t in range(start,end):
            number_persons_pers = 0
           
            for (st,rate,ft) in seq:
                if (t>=st and t<(st+ft)):
                    number_persons = number_persons+ rate
           
            if (number_persons>capacity):
            
                valid = False
                conflicts.add(a)
    return (valid,conflicts)

if __name__== "__main__":
    dataname = sys.argv[1]
    solname = sys.argv[2]
    pathfile = "../"
    (my_evacuation,my_graph) = read.read_data(pathfile + dataname)
    my_solution = read.read_solution(pathfile + solname)
    print("solution: ", my_sol)
    if verify_max_rates(my_evacuation,my_graph,my_sol['param']):
        print("Evacuation rate is okay")
    else:
        print("Evacuation rate is not okay")
    gantt_blocs = create_blocs(my_evac,my_graph,my_sol['param'])
    print("Bloc representation for the solution ", gantt_blocs)
    print("theoretical objective = " , my_sol['objective'], " minimum objective = ", objective_Calculation(my_evac,gantt_blocs))
    feasible = capacity_verification(my_evac,my_graph,gantt_blocs)
    if feasible:
        print("It is a feasible solution")
    else:
        print("It is not a feasible solution")
