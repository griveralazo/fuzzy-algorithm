from collections import Counter

from pm4py import util as pmutil
from pm4py.objects.log.util import xes as xes_util

WINDOW = "window"
DEFAULT_WINDOW = 1


def apply(log, parameters=None):
    print("native")
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
    if parameters is None:
        parameters = {}
    if pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY not in parameters:
        parameters[pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = xes_util.DEFAULT_NAME_KEY

    window = parameters[WINDOW] if WINDOW in parameters else DEFAULT_WINDOW
    activity_key = parameters[pmutil.constants.PARAMETER_CONSTANT_ACTIVITY_KEY]
    dfgs = map((lambda t: [(t[i - window][activity_key], t[i][activity_key]) for i in range(window, len(t))]), log)
    return Counter([dfg for lista in dfgs for dfg in lista])
