import sys
import time
import copy
from operator import itemgetter
import read_data as read
import Verification_Solution as VeSo
import Creation_file_Solution as CfSo


if __name__== "__main__":
    dataname = sys.argv[1]
    solname = sys.argv[2]
   
    datapathfile = "../InstancesInt/"  # pathfile = "../"
    solutionpathfile = "../Solutions/"
    (my_evac,my_graph) = read.read_data(datapathfile + dataname)
    sol_finale = (my_evac,my_graph)
    
    print("Previous Objective: ",sol_initiale['objective'], " New objective:", sol_finale[1])