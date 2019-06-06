import sys
import os
import time
import copy
import random
from operator import itemgetter
import Read_data as read
import Verification_Solution as VeSo
import Creation_File_solution as CfSo

def Neighbour_date(evacuation_nodes,arcs,blocs,step):
   #Calculation of time of evacuation of every node
    temps_evac = [(x,(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evacuation_nodes]
         # Get the node that takes the longest time
    node_limit = max(evac_time,key=itemgetter(1))
       # Start the evacuation one step earlier
    if (blocs[(node_limit[0],evacuation_nodes[node_limit[0]]['route'][0])][0] - step) >= 0:
        new_blocs = copy.deepcopy(blocs)
        for arc in evacuation_nodes[node_limit[0]]['route']:
            new_blocs[(node_limit[0],arc)] = (new_blocs[(node_limit[0],arc)][0] - step,new_blocs[(node_limit[0],arc)][1])
        new_blocs[(node_limit[0],(evacuation_nodes[node_limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_limit[0],(evacuation_nodes[node_limit[0]]['route'][-1][1],'completed'))][0] - step,new_blocs[(node_limit[0],(evacuation_nodes[node_limit[0]]['route'][-1][1],'completed'))][1])
        # if the solution created is feasible, it is a neighbour
        if VeSo.Capacity_Verification(evacuation_nodes,arcs,new_blocs):
            
            return (True,new_blocs)
         # otherwise we try to move the second longest one forward
        else:
           
            evac_time.remove(node_limit)
            node_aux = max(evac_time,key=itemgetter(1))
            if (blocs[(node_aux[0],evacuation_nodes[node_aux[0]]['route'][0])][0] - step) >= 0:
                for arc in evacuation_nodes[node_aux[0]]['route']:
                    new_blocs[(node_aux[0],arc)] = (new_blocs[(node_aux[0],arc)][0] - step,new_blocs[(node_aux[0],arc)][1])
                new_blocs[(node_aux[0],(evacuation_nodes[node_aux[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_aux[0],(evacuation_nodes[node_aux[0]]['route'][-1][1],'completed'))][0] - step,new_blocs[(node_aux[0],(evacuation_nodes[node_aux[0]]['route'][-1][1],'completed'))][1])
                 #if the created solution is feasible, it is a neighbour
                ifVeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs):
                    
                    return (True,new_blocs)
               
                else:
                   
                    return (False,{})
            else:
              
                return (False,{})
   
    else:
        
        return (False,{})

def Neighbour_rate(evacuation_nodes,arcs,blocs,step):
   #Calculation of time of evacuation of every node
    evac_time = [(x,(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evacuation_nodes]
    
    node_limit = max(evac_time,key=itemgetter(1))
    
    possible_max_rate = min(evacuation_nodes[node_limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evacuation_nodes[node_limit[0]]['route']]))
    current_rate = blocs[(node_limit[0],evacuation_nodes[node_limit[0]]['route'][0])][1]
   
    if (current_rate + step) <= possible_max_rate:
        new_blocs = copy.deepcopy(blocs)
        for arc in evacuation_nodes[node_Limit[0]]['route']:
            new_blocs[(node_Limit[0],arc)] = (new_blocs[(node_Limit[0],arc)][0],current_rate + step)
        new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][0],current_rate + step)
       #If the solution created is feasible, it is a neighbour
        (ok,conflits) = VeSo.capacity_Verification_with_return(evacuation_nodes,arcs,new_blocs)
        if ok:
           
            return (True,new_blocs)
        
        else:
           
            node_conflicts = set([tup[0] for tup in blocs if tup[1] in conflicts])
            node_conflicts.discard(node_limit[0])
           
            for x in node_conflicts:
                if new_blocs[(x,evacuation_nodes[x]['route'][0])][1] - step > 0:
                    new_blocs[(x,evacuation_nodes[x]['route'][0])] = (new_blocs[(x,evacuation_nodes[x]['route'][0])][0], new_blocs[(x,evacuation_nodes[x]['route'][0])][1] - step)
           
            if VeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs):
                # print("rate increase with OK adjustments")
                return (True,new_blocs)
            #Or stop
            else:
                # print("rate increase with adjustments NOT OK")
                return (False,{})
    # if not no neighbor --> try with the second one later and advance the departure dates
    else:
        return (False,{})

def Neighbour_rate_date(evacuation_nodes,arcs,blocs,step,nb_temp_steps=-1):
   #Calculation of time of evacution of every node
    evac_time = [(x,(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evacuation_nodes]
   
    node_limit = max(evac_time,key=itemgetter(1))
   
    possible_max_rate = min(evacuation_nodes[node_limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evacuation_nodes[node_limit[0]]['route']]))
    current_rate = blocs[(node_limit[0],evacuation_nodes[node_limit[0]]['route'][0])][1]
   
    if (current_rate + step) <= possible_max_rate:
        new_blocs = copy.deepcopy(blocs)
        for arc in evacuation_nodes[node_limit[0]]['route']:
            new_blocs[(node_limit[0],arc)] = (new_blocs[(node_limit[0],arc)][0],current_rate + step)
        new_blocs[(node_limit[0],(evacuation_nodes[node_limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_limit[0],(evacuation_nodes[node_limit[0]]['route'][-1][1],'completed'))][0],current_rate + step)
        
        (ok,conflicts) = VeSo.capacity_Verification_with_return(evacuation_nodes,arcs,new_blocs)
        if ok:
            # print("OK rate increase")
            return (True,new_blocs)
        # otherwise we try to decrease the rate of conflicting nodes by the step value to compensate
        else:
           # print("rate increase NOT OK")
            node_conflicts = set([tup[0] for tup in blocs if tup[1] in conflicts])
            node_conflicts.discard(node_limit[0])
           
            for x in node_conflicts:
                if new_blocs[(x,evacuation_nodes[x]['route'][0])][1] - step > 0:
                    new_blocs[(x,evacuation_nodes[x]['route'][0])] = (new_blocs[(x,evacuation_nodes[x]['route'][0])][0], new_blocs[(x,evacuation_nodes[x]['route'][0])][1] - step)
            # if the solution created is feasible, it is a neighbour
            if VeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs):
                # print("rate increase with OK adjustments")
                return (True,new_blocs)
           # otherwise the start date of the modified node is postponed to obtain a feasible solution
            else:
                # print("rate increase with adjustments NOT OK --> delays departure")
                # the departure date is postponed by 1 until the solution is feasible
                solution_found = False
                if (nb_temp_steps < 0):
                    # print("start delayed until solution")
                    while not solution_found:
                        for arc in evacuation_nodes[node_limit[0]]['route']:
                            new_blocs[(node_limit[0],arc)] = (new_blocs[(node_limit[0],arc)][0]+1,new_blocs[(node_limit[0],arc)][1])
                        new_blocs[(node_limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][0]+1,new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][1])
                        solution_found = VeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs)
                else:
                   # print("start delays until threshold reached or solution")
                    i = 0
                    while (i < nb_time_steps and  not solution_found):
                        for arc in evacuation_nodes[node_Limit[0]]['route']:
                            new_blocs[(node_Limit[0],arc)] = (new_blocs[(node_Limit[0],arc)][0]+1,new_blocs[(node_Limit[0],arc)][1])
                        new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][0]+1,new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][1])
                        solution_found =VeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs)
                        i = i + 1
                if solution_found:
                    # print("move date OK")
                    return (True,new_blocs)
                else:
                     # print("move date NOT OK")
                    return (False,{})
    # if not no neighbor --> try with the second one later and advance the departure dates
    else:
        # print("no neighbors generated")
        return (False,{})

def  Neighbor_rate_and_date(evacuation_nodes,arcs,blocs,step_rate,step_date):
    # calculation of the evacuation time of each node

    evac_time = [(x,(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evacuation_nodes]
    # Get the node that takes the longest time
    node_Limit = max(evac_time,key=itemgetter(1))
    
   # we get the maximum possible rate for the node and the rate of the solution taken
    possible_max_rate = min(evacuation_nodes[node_Limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evacuation_nodes[node_Limit[0]]['route']]))
    current_rate = blocs[(node_Limit[0],evacuation_nodes[node_Limit[0]]['route'][0])][1]
    # if possible, we try to increase its evacuation rate by the step value
    if (current_rate + step_rate) <= possible_max_rate:
        new_blocs = copy.deepcopy(blocs)
        for arc in evacuation_nodes[node_Limit[0]]['route']:
            new_blocs[(node_Limit[0],arc)] = (new_blocs[(node_Limit[0],arc)][0],current_rate + step_rate)
        new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][0],current_rate + step_rate)
        # if the solution created is feasible, we try to bring forward the start date
        ifVeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs):
            print("augmentation rate is OK")
            blocs_ok = copy.deepcopy(new_blocs)
            if (blocs[(node_Limit[0],evacuation_nodes[node_Limit[0]]['route'][0])][0] - step_date) >= 0:
                for arc in evacuation_nodes[node_Limit[0]]['route']:
                    new_blocs[(node_Limit[0],arc)] = (new_blocs[(node_Limit[0],arc)][0]- step_date,new_blocs[(node_Limit[0],arc)][1])
                new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))] = (new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][0] - step_date,new_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][1])
           # if the new solution created is feasible, it is a neighbour
            ok =VeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs)
            if ok:
                print("Forward date OK")
                return (True,new_blocs)
            # otherwise we keep the previous one
            else:
                print("Forward date is not OK")
                return(True,blocs_ok)
        # otherwise we're trying to move up the departure date
        else:
            print("augmentation rateis not OK")
            n_blocs = copy.deepcopy(blocs)
            if (blocs[(node_Limit[0],evacuation_nodes[node_Limit[0]]['route'][0])][0] - step_date) >= 0:
                for arc in evacuation_nodes[node_Limit[0]]['route']:
                    n_blocs[(node_Limit[0],arc)] = (n_blocs[(node_Limit[0],arc)][0]- step_date,n_blocs[(node_Limit[0],arc)][1])
                n_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))] = (n_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][0] - step_date, n_blocs[(node_Limit[0],(evacuation_nodes[node_Limit[0]]['route'][-1][1],'completed'))][1])
                # if the new solution created is feasible, it is a neighbour
                if VeSo.capacity_Verification(evacuation_nodes,arcs,n_blocs):
                    print("Forward date OK")
                    return (True,n_blocs)
              #otherwise Stop
                else:
                    print("Forward date is not OK")
                    return (False,{})
            else:
                print("Forward date is not OK")
                return (False,{})
    #otherwise no neighbor
    else:
        print("no neighbor is generated")
        return (False,{})

# Function that allows you to choose the first best neighbor by changing only the dates
def choice_first_neighbor_date(evacuation_nodes,arcs,blocs,eval_prev):
   # we loop until we reach 0 and find a better neighbor
    keep_search = True
    best_neighbor = {}
    while keep_search:
        # Generation of neighbor
        (possible,neighbor) = neighbor_date(evacuation_nodes,arcs,blocs,1)
       #if the solution is feasible, we can evaluate
        if possible:
            
            eval_neighbor = VeSo.calculate_objective(evacuation_node,neighbor)
            # if the evaluation of this new neighbor is better than the one in parameter (eval_prev) we return it
            if eval_neighbor <= eval_prev:
                
                keep_search = False
                best_neighbor = neighbor
            #otherwise we continue
            else:
                
                keep_search = True
        #otherwise stop
        else:
           
            keep_search = False
    return best_neighbor

# Function that allows you to choose the first best neighbor by changing only the evacuation rates
def choice_first_neighbor_rate(evacuation_nodes,arcs,blocs,eval_prev):
    # calculation of the evacuation time of each node
    evac_time = [(x,(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evacuation_nodes]
    # Get the node that takes the longest time
    node_Limit = max(evac_time,key=itemgetter(1))
    # we get the maximum possible rate for the node and the rate of the solution taken
    max_rate_node_limit = min(evacuation_nodes[node_Limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evacuation_nodes[node_Limit[0]]['route']]))
    current_rate = blocs[(node_Limit[0],evacuation_nodes[node_Limit[0]]['route'][0])][1]
    # we try to increase the slowest node to its maximum evacuation rate
    step = max_rate_node_limit - current_rate
    # we loop until we reach the maximum rate and find a better neighbor
    keep_search = step > 0
    best_neighbor = {}
    while keep_search:
       # print("generate neighbor with step:", step)
        # generation of a neighbor
        (possibl,neighbor) = neighbor_rate(evacuation_nodes,arcs,blocs,step)
        # if the solution is feasible, it is evaluated
        if possible:
            # print("neighbor found")
            eval_neighbor = VeSo.calculate_objective(evacuation_node,neighbor)
            # if the evaluation of this new neighbor is better than the one in parameter (eval_prev) we return it
            if eval_neighbor < eval_prev:
                # print("First neighbor exploration found")
                keep_search = False
                best_neighbor = neighbor
            # Or we reduce the valeue of augmentation
            else:
                # print("neighbor non explorable--> we reduce the step")
                step = step - 1
                keep_search = step > 0
        # if the solution is not feasible, the increase value is reduced
        else:
            # print("neighbor not found --> we reduce the step")
            step = step - 1
            keep_search = step > 0
    return best_neighbor

# Function that allows you to choose the first best neighbor by changing the rate and then the evacuation date
def choice_first_neighbor_rate_and_date(evacuation_nodes,arcs,blocs,eval_prev):
   # calculation of the evacuation time of each node
    evac_time = [(x,(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evacuation_nodes]
   # Get the node that takes the longest time
    node_Limit = max(evac_time,key=itemgetter(1))
    # we get the maximum possible rate for the node and the rate of the solution taken
    max_rate_node_limit = min(evacuation_nodes[node_Limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evacuation_nodes[node_Limit[0]]['route']]))
    current_rate = blocs[(node_Limit[0],evacuation_nodes[node_Limit[0]]['route'][0])][1]
    # we try to increase the slowest node to its maximum evacuation rate
    step = max_rate_node_limit - current_rate
    # we loop until we reach the maximum rate and find a better neighbor
    keep_search = step > 0
    best_neighbor = {}
    while keep_search:
        
        # generation of a neighbor
        (possible,neighbor) = neighbor_rate_then_date(evacuation_nodes,arcs,blocs,step,1)
        # if the solution is feasible, it is evaluated
        if possible:
            # print("neighbor found")
            eval_neighbor = VeSo.calculate_objective(evacuation_node,neighbor)
            # if the evaluation of this new neighbor is better than the one in parameter (eval_prev) we return it
            if eval_neighbor < eval_prev:
                # print("first improving neighbor found")
                keep_search = False
                best_neighbor = neighbor
            # otherwise we reduce the value of the increase
            else:
                # print("neighbor non explorablet --> we reduce the step")
                step = step - 1
                keep_search = step > 0
          # if the solution is not feasible, the increase value is reduced
         else:
           
            step = step - 1
            keep_search = step > 0
    return best_neighbor

# Function that allows you to choose the first best neighbor by changing evacuation rates and dates

def choice_first_neighbor_rate_date(evacuation_nodes,arcs,blocs,eval_prev):
   # calculation of the evacuation time of each node
    evac_time = [(x,(blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][0] - (-evacuation_nodes[x]['pop']//blocs[(x,(evacuation_nodes[x]['route'][-1][1],'completed'))][1]))) for x in evacuation_nodes]
    # Get the node that takes the longest time
    node_Limit = max(evac_time,key=itemgetter(1))
    # we get the maximum possible rate for the node and the rate of the solution taken
    max_rate_node_limit = min(evacuation_nodes[node_Limit[0]]['max_rate'],min([arcs[arc]['capacity'] for arc in evacuation_nodes[node_Limit[0]]['route']]))
    current_rate = blocs[(node_Limit[0],evacuation_nodes[node_Limit[0]]['route'][0])][1]
       # we try to increase the slowest node to its maximum evacuation rate
    step = max_rate_node_limit - current_rate
    # we loop until we reach the maximum rate and find a better neighbor
    keep_search = step > 0
    best_neighbor = {}
    while keep_search:
        
        # generation of a neighbor
       #by advancing the date by a maximum of the step value --> to be adjusted
        (possibl,neighbor) = neighbor_rate_date(evacuation_nodes,arcs,blocs,step,step)
       # (possibl,neighbor) = neighbor_rate_date(evacuation_nodes,arcs,blocks,step)
        # if the solution is feasible, it is evaluated
        if possible:
            # print("neighbor found")
            eval_neighbor = VeSo.calculate_objective(evacuation_node,neighbor)
            # if the evaluation of this new neighbor is better than the one in parameter (eval_prev) we return it
            if eval_neighbor < eval_prev:
                # print("First neighbor exploring found")
                keep_search = False
                best_neighbor = neighbor
           #or we reduce the value of augmentation
            else:
                # print("neighbor non explorable --> we reduce the step")
                step = step - 1
                keep_search = step > 0
       # if the solution is not feasible, the increase value is reduced
        else:
            # print("neighbor not found--> we reduce the step")
            step = step - 1
            keep_search = step > 0
    return best_neighbor

def diversification_date(evacuation_nodes,arcs,blocs,step):
    # creation of a feasible solution by randomly changing departure dates
    solution_found = False
    new_blocs = copy.deepcopy(blocs)
    while not solution_found:
        print("modification random")
        # choise of a random node
        r0 = random.choice(list(evacuation_nodes.keys()))
        rand_node = (r0, evacuation_nodes[r0])
        current_date = new_blocs[(rand_node[0],evacuation_nodes[rand_node[0]]['route'][0])][0]
        rand_val = random.randint(1,step)
       # add a random value to its start date
        for arc in evacuation_nodes[rand_node[0]]['route']:
            new_blocs[(rand_node[0],arc)] = (new_blocs[(rand_node[0],arc)][0] + rand_val,new_blocs[(rand_node[0],arc)][1])
        new_blocs[(rand_node[0],(evacuation_nodes[rand_node[0]]['route'][-1][1],'completed'))] = (new_blocs[(rand_node[0],(evacuation_nodes[rand_node[0]]['route'][-1][1],'completed'))][0] + rand_val, new_blocs[(rand_node[0],(evacuation_nodes[rand_node[0]]['route'][-1][1],'completed'))][1])
        solution_found =VeSo.capacity_Verification(evacuation_nodes,arcs,new_blocs)
    # print("solution random: ", new_blocs)
    return new_blocs

# The initial solution is an upper bound of evacuation rates with the departure date at 0
def local_search(evacuation_nodes,arcs,sol_init,name,path_sol):
    start_time = time.time()
    # initial solution
    one_sol =VeSo.create_blocs(evacuation_nodes,arcs,sol_init['param'])
    one_eval = sol_init['objective']
    best_sol = copy.deepcopy(one_sol)
    best_eval = one_eval
    # stop when you can't find any more improving neighbors
    condition_stop = False
    # repeat
    while not condition_stop:
        neighbor = choice_first_neighbor_rate(evacuation_nodes,arcs,one_sol,one_eval)
        
        if neighbor :
            # print("neighbor exploration is generated")
            condition_stop = False
            one_sol = neighbor
            one_eval =VeSo.calculate_objective(evacuation_nodes,one_sol)
            if one_eval < best_eval:
                best_sol = copy.deepcopy(one_sol)
                best_eval = one_eval
        else:
            # print("No neighbor exploration --> End of local search")
            condition_stop = True
    end_time = time.time()
    #Creation of file solution
    params_sol = {}
    for x in evacuation_nodes:
        params_sol[x] = (best_sol[(x,evacuation_nodes[x]['route'][0])][1],best_sol[(x,evacuation_nodes[x]['route'][0])][0])
    valid =VeSo.capacity_Verification(evacuation_nodes,arcs,best_sol)
    if valid:
        nature_sol = "valid"
    else:
        nature_sol = "invalid"
    fs.write_solution(name, params_sol, nature_sol, best_eval, end_time-start_time, "local search with increased evacuation rate and date of departure","First trial",path_sol)
    return (best_sol,best_eval)

     # The initial solution is an upper bound of evacuation rates with the departure date at 0
    def Local_Search_div(evacuation_nodes,arcs,sol_init,name,path_sol,nb_iterations):
     
    
    start_time = time.time()
    # Initial solution
    one_sol =VeSo.create_blocs(evacuation_nodes,arcs,sol_init['param'])
    one_eval = sol_init['objective']
    best_sol = copy.deepcopy(one_sol)
    best_eval = one_eval
    #Lists of best solution found
    list_best_sol = []
    # stop after a certain number of iterations
    i = 0
   
    # step for the diversification
    step = 10
    # repeat
    while i < nb_iterations:
        neighbor_found = True
        while neighbor_found:
            neighbor = choice_first_neighbor_rate_and_date(evacuation_nodes,arcs,one_sol,one_eval)
            if neighbor :
                print("neighbor exploration is generated")
                one_sol = neighbor
                one_eval =VeSo.calculate_objective(evacuation_nodes,one_sol)
                if one_eval < best_eval:
                    best_sol = copy.deepcopy(one_sol)
                    best_eval = one_eval
            else:
                print("No neighbor explorations --> diversification iteration n° ",i)
                neighbor_found = False
       # we add the best solution found
        list_best_sol.append((best_eval,best_sol))
        i = i + 1
        # we add random --> step to adjust
        one_sol = diversification_date(evacuation_nodes,arcs,one_sol,step)
        one_eval =VeSo.calculate_objective(evacuation_nodes,one_sol)
    print("list_best_sol: ", list_best_sol)
    (best_obj, best_solution) = min(list_best_sol,key=itemgetter(0))
    end_time = time.time()
    # Creation of file solution
    params_sol = {}
    for x in evacuation_nodes:
        params_sol[x] = (best_solution[(x,evacuation_nodes[x]['route'][0])][1],best_solution[(x,evacuation_nodes[x]['route'][0])][0])
    valid =VeSo.capacity_Verification(evacuation_nodes,arcs,best_solution)
    if valid:
        nature_sol = "valid"
    else:
        nature_sol = "invalid"
    fs.write_solution(name, params_sol, nature_sol, best_obj, end_time-start_time, "local search with increased evacuation rate and dates of departure",path_sol)
    return (best_solution,best_obj)

if __name__== "__main__":
    dataname = sys.argv[1]
    solname = sys.argv[2]
    # pathfile = "../"
    datapathfile = "../InstancesInt/"
    solutionpathfile = "../Solutions/"
    (my_evac,my_graph) = read.read_data(datapathfile + dataname)
    sol_initial= read.read_solution(solutionpathfile + solname)
    # sol_final = Local_Search(my_evac,my_graph,sol_initial, os.path.splitext(dataname)[0],"../Solutions/Intens_rate_and_date/")
    sol_finale =Local_Search_with_div(my_evac,my_graph,sol_initiale, os.path.splitext(dataname)[0],"../Solutions/IntensDiv0/",15)
   # print("best solution:", sol_final[0], "with objective:", sol_final[1])
    print("Old objective: ",sol_initial['objective'], " New objective:", sol_final[1])
