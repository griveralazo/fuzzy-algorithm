from collections import Counter
"""
from pm4py import util as pmutil
from pm4py.objects.log.util import xes as xes_util
"""
def apply(log, parameters=None):
    """
    Counts the number of directly follows occurrences, i.e. of the form <...a,b...>, in an event log.

    Parameters
    ----------
    log
        Trace log
    parameters
        Possible parameters passed to the algorithms:
            activity_key -> Attribute to use as activity

    Returns
    -------
    dfg
        DFG graph
    """
    """
    if parameters is None:
        parameters = {}
    if pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY not in parameters:
        parameters[pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = xes_util.DEFAULT_NAME_KEY
    """
    #activity_key = parameters[pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY]
    activity_key = 0
    
    dfgs = list(map((lambda t: [(log[t][i - 2][activity_key], log[t][i - 1][activity_key], log[t][i][activity_key]) for i in range(2, len(log[t]))]), log))
    #print("dfgs: ", dfgs)
    
    counter = {}
    for i in dfgs:
        #print(i)
        for j in i:
            if j in counter:
                counter[j] = counter[j] + 1
            else:
                counter[j] = 1
    return counter
    #return Counter([dfg for lista in dfgs for dfg in lista])