from ConnectionData import ConnectionData
import pandas as pd
import sqlalchemy as sql

from pm4py.algo.discovery.heuristics import factory as heuristics_miner
from fuzzy import Fuzzy
import time;

#from pm4py.objects.log.importer.xes import factory as xes_importer
#from pm4py.visualization.heuristics_net import factory as hn_vis_factory
#from pm4py.visualization.petrinet import factory as petri_vis_factory


def execute_script():
    t1 = time.time()
    f = Fuzzy()
    Data = ConnectionData()
    connect_string = Data.get_connection_string()
    sql_engine = sql.create_engine(connect_string)
    query = Data.get_query()
    
    df = pd.read_sql_query(query, sql_engine)
    log = df
    t2 = time.time()

    heu_net = heuristics_miner.apply_heu(log, parameters={"dependency_thresh": 0.99})
    t3 = time.time()
    f = Fuzzy()
    preservethereshold = 0.6
    ratiothereshold = 0.7 #default values taken from PROM, but they are variables
    
    heu_net = f.relation(heu_net, preservethereshold, ratiothereshold)
    t4 = time.time()
    
    """
    for k in heu_net.new_dfg:
        print(k, heu_net.new_dfg[k])
    print("************************")
    for k in heu_net.performance_dfg:
        print(k, heu_net.performance_dfg[k])
    """
    utilityrt = 0.75
    cutoff = 0.2 #default values taken from PROM, but they are variables
    
    heu_net = f.edge_filter(heu_net, utilityrt, cutoff, log)
    t5 = time.time()
    """
    for k in heu_net.new_dfg:
        print(k, heu_net.new_dfg[k])
    print("************************")
    for k in heu_net.ProximityCorrelationQuantity:
        print(k, heu_net.ProximityCorrelationQuantity[k])
    print("########################")
    """
    nodeCutoff = 0.75   
    lst = f.aggregation(heu_net, nodeCutoff)
    t6 = time.time()
    
    unaryCorrelation = f.getunaryCorrelation(heu_net.activities_occurrences)
    
    print("something something: ", len(lst[1]))
    print("survivors: ")
    for k in lst[0]:
        print("predecesors:  ",k.get_predecessors())
        print("successors:   ",k.get_successors())
        print("elements:     ",k.get_elements())
        print("Is victim:    ", k.is_cluster())
        print("Significance: ", k.defsignificance(unaryCorrelation))
        print()
    print("#################################")
          
    print("survivors.......?: ")
    for k in lst[1]:
        print("predecesors:  ",k.get_predecessors())
        print("successors:   ",k.get_successors())
        print("elements:     ",k.get_elements())
        print("Is victim:    ", k.is_cluster())
        print("Significance: ", k.defsignificance(unaryCorrelation))
        print()
    print("#################################")
          
    print("**********************************")
    print("**********************************")
    print("**********************************")
    print("Tiempo total de ejecución:               ", t6 - t1)
    print("Tiempo de conexión a la DB:              ", t2 - t1)
    print("Tiempo del heuristic miner:              ", t3 - t2)
    print("Tiempo del conflict resolution:          ", t4 - t3)
    print("Tiempo del edge filtering:               ", t5 - t4)
    print("Tiempo del aggregation and abstraction:  ", t6 - t5)
    """
    we have the value of the relation, so it can be filtered.
    """
    """
    gviz = hn_vis_factory.apply(heu_net, parameters={"format": "svg"})
    hn_vis_factory.view(gviz)
    net, im, fm = heuristics_miner.apply(log, parameters={"dependency_thresh": 0.99})
    gviz2 = petri_vis_factory.apply(net, im, fm, parameters={"format": "svg"})
    petri_vis_factory.view(gviz2)
    """
    """
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    unaryCorrelation = f.getunaryCorrelation(heu_net.activities_occurrences)
    for k in unaryCorrelation:
        print(k, unaryCorrelation[k])
        
    """
    print()
    print()
    print()
    print()
    for j in heu_net.performance_dfg:
       print(j, heu_net.performance_dfg[j])
    
    print()
    print()
    print()
    print(dir(heu_net))
    

if __name__ == "__main__":
    execute_script()

"""
len all:  ['start_timestamp_2', 'start_timestamp', 'case_id', 'case_id_2']
Traceback (most recent call last):
    
"""