# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:35:53 2019

@author: jgonz
"""

class ConnectionData:
    connect_string = 'postgresql://postgres:grespost2@68.183.81.155/postgres'
    query = "SELECT * from table_3"
    def get_connection_string(self):
        return self.connect_string
    def get_query(self):
        return self.query
    