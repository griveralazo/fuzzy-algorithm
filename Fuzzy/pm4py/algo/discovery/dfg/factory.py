import pandas

#from pm4py import util as pmutil
from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.discovery.dfg.versions import native, performance, freq_triples
from pm4py.objects.conversion.log import factory as log_conversion
from pm4py.objects.log.adapters.pandas import csv_import_adapter
#from pm4py.objects.log.util import general as log_util
#from pm4py.objects.log.util import xes as xes_util

DFG_NATIVE = 'native'
DFG_FREQUENCY = 'frequency'
DFG_PERFORMANCE = 'performance'
DFG_FREQUENCY_GREEDY = 'frequency_greedy'
DFG_PERFORMANCE_GREEDY = 'performance_greedy'
FREQ_TRIPLES = 'freq_triples'

VERSIONS = {DFG_NATIVE: native.apply, DFG_FREQUENCY: native.apply, DFG_PERFORMANCE: performance.apply,
            DFG_FREQUENCY_GREEDY: native.apply, DFG_PERFORMANCE_GREEDY: performance.apply,
            FREQ_TRIPLES: freq_triples.apply}


def apply(log, parameters=None, variant=DFG_NATIVE):
    if variant == 'performance':
        performance = True
    else:
        performance = False
    """
    Calculates DFG graph (frequency or performance) starting from a log

    Parameters
    ----------
    log
        Log
    parameters
        Possible parameters passed to the algorithms:
            aggregationMeasure -> performance aggregation measure (min, max, mean, median)
            activity_key -> Attribute to use as activity
            timestamp_key -> Attribute to use as timestamp
    variant
        Variant of the algorithm to use, possible values:
            native, frequency, performance, frequency_greedy, performance_greedy

    Returns
    -------
    dfg
        DFG graph
    """
    if parameters is None:
        parameters = {}

    PARAMETER_CONSTANT_ACTIVITY_KEY = 'PARAMETER_CONSTANT_ACTIVITY_KEY'
    PARAMETER_CONSTANT_TIMESTAMP_KEY = 'PARAMETER_CONSTANT_TIMESTAMP_KEY'
    PARAMETER_CONSTANT_CASEID_KEY = 'PARAMETER_CONSTANT_CASEID_KEY'

    parameters[PARAMETER_CONSTANT_ACTIVITY_KEY] = 2
    parameters[PARAMETER_CONSTANT_TIMESTAMP_KEY] = 1
    parameters[PARAMETER_CONSTANT_CASEID_KEY] = 0
    
    if isinstance(log, pandas.core.frame.DataFrame):
        log = csv_import_adapter.convert_timestamp_columns_in_df(log, timest_columns=[
            parameters[PARAMETER_CONSTANT_TIMESTAMP_KEY]])
        dfg_frequency, dfg_performance = df_statistics.get_dfg_graph(log, measure="both",
                                                                     activity_key=parameters[
                                                                         PARAMETER_CONSTANT_ACTIVITY_KEY],
                                                                     timestamp_key=parameters[
                                                                         PARAMETER_CONSTANT_TIMESTAMP_KEY],
                                                                     case_id_glue=parameters[
                                                                         PARAMETER_CONSTANT_CASEID_KEY])
        
        if performance == True:
            return dfg_performance
        
        if 'native' in variant or 'frequency' in variant:
            return dfg_frequency
        else:
            if variant == 'freq_triples':
                return freq_triples.apply(log, parameters)
            return dfg_performance
    return freq_triples.apply(log, parameters)
    #return VERSIONS[variant](log_conversion.apply(log, parameters, log_conversion.TO_EVENT_LOG), parameters=parameters)
