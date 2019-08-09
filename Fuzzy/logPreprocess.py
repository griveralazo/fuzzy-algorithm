# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:39:25 2019

@author: jgonz
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:13:57 2019

@author: jgonz
"""
import pandas as pd
import sqlalchemy as sql


"""
class LogPreprocessor:
    def preProcessLog(self, df):
        log = {}
        for index, row in df.iterrows():
            activity = list()
            activity.append(row.activity)
            activity.append(row.start_timestamp)
            activity.append(row.complete_timestamp)
            activity.append(row.resource)
            activity.append(row.role)
#            activity.append(row.Price)
#            activity.append(row.Item)
#            activity.append(row.proveedor)
#            activity.append(row.purchasinggroup)
#            activity.append(row.sueldo)
            event_key = row.case_id
            if event_key in log:
                log[event_key].append(activity)
            else:
                case = list()
                case.append(activity)
                log[event_key] = case
        for akey in log:
            sorted(log[akey], key=lambda x: x[1])
            #log[akey].sort(key = lambda x: x[1])
        return log
   """
"""
connect_string = 'postgresql://postgres:jgonzalez@159.65.78.54/postgres'

sql_engine = sql.create_engine(connect_string)

query =query = "select * from PurchasingExample"
df = pd.read_sql_query(query, sql_engine)
            
lala = LogPreprocessor()
for akey in lala.preProcessLog(df):
    print akey
    for k in lala.preProcessLog(df)[akey]:
        print k
        print "\n"
    print "\n\n"
"""