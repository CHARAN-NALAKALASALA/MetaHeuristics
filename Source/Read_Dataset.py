import sys

def read_dataset(filename):
    evac_info = {} #evac_info={evac_node_id : {'pop':.., 'max_rate':.., 'k':.., 'route':[(id,node1),(node1,node2),..]} }
    graph = {} #graph = {(node1,node2):{'duedate':.., 'length':.., 'capacity':..}}
    f = open(filename,"r")
    line = f.readline()
    if (line.startswith("c [evacuation info]")):
        line = f.readline()
        ll = line.split()
        num_evac_nodes = int(ll[0])
        id_safe_node = int(ll[1])
        for i in range(num_evac_nodes):
            line = f.readline()
            ll = line.split()
            id = int(ll[0])
            pop = int(ll[1])
            max_rate = int(ll[2])
            k = int(ll[3])
            vl = []
            prev = id
            for j in range(4,4+k):
                ni = int(ll[j])
                if prev < ni :
                    vl.append((prev,ni))
                else:
                    vl.append((ni,prev))
                prev = ni
            '''Information we have node to:
                    population
                    maximum evacuation speed
                    number of nodes through which it must pass to evacuate it
                    nodes through which it is necessary to pass to evacuate it
            '''
            evac_info[id] = {'pop': pop, 'max_rate': max_rate, 'k': k, 'route': vl}
        # print(evac_info)
    line = f.readline()
    if (line.startswith("c [graph]")):
        line = f.readline()
        ll = line.split()
        num_nodes = int(ll[0])
        num_edges = int(ll[1])
        for i in range(num_edges):
            line = f.readline()
            ll = line.split()
            n1 = int(ll[0])
            n2 = int(ll[1])
            duedate = int(ll[2])
            length = int(ll[3])
            capacity = int(ll[4])
            ''' Information about a given arc:
                    deadline date
                    length (which leads to trivial travel time)
                    capacity
            '''
            if (n1<n2):
                graph[(n1,n2)] = {'due_date': duedate, 'length': length, 'capacity': capacity}
            else:
                graph[(n2,n1)] = {'due_date': duedate, 'length': length, 'capacity': capacity}
        # print(graph)
    return (evac_info,graph)

def read_solution(filename):
    f = open(filename,"r")
    sol_info = {}
    line = f.readline()
    sol_info['solution_name'] = line.rstrip('\n')
    line = f.readline()
    sol_info['nb_evacuation_nodes'] = int(line)
    node_info = {}
    ll = []
    for i in range(sol_info['nb_evacuation_nodes']):
        line = f.readline()
        ll = line.split()
        node_info[int(ll[0])] = (int(ll[1]),int(ll[2]))
    sol_info['param'] = node_info
    line = f.readline()
    sol_info['nature'] = line.rstrip('\n')
    line = f.readline()
    sol_info['objective'] = int(line)
    line = f.readline()
    sol_info['processing_time'] = float(line)
    line = f.readline()
    sol_info['method'] = line.rstrip('\n')
    line = f.readline()
    sol_info['how'] = line.rstrip('\n')
    return sol_info

def main():
    pathfile = "../InstancesInt/"
    dataname = sys.argv[1]
    solname = sys.argv[2]
    # pathfile = "../"
    print("in main, run read_data")
    (my_evac,my_graph) = read_data(pathfile + dataname)
    print("my graph ", my_graph)
    print("my evac info ", my_evac)
    my_sol = read_solution(pathfile + solname)
    print("my sol ",my_sol)

if __name__== "__main__":
  main()