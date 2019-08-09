# -*- coding: utf-8 -*-
"""
Created on Mon May 20 03:29:53 2019

@author: jgonz
"""

class Node:
    def __init__(self, activity, nodeType, usignificance):
        self.predecessors = []
        self.successors = []
        self.nodeType = nodeType #Cluster or activity
        self.itself = [activity] #If activity, then there is only one element in the list
        self.unarySignificance = usignificance
        
    def getUnarySignificance(self, uS):
        self.unarySignificance
        
    def is_cluster(self):
        if self.nodeType== "Cluster":
            return True
        else:
            return False
        
    def get_elements(self):
        return self.itself
    
    def get_predecessors(self):
        return self.predecessors
    
    def get_successors(self):
        return self.successors
    
    def append_predecessor(self, previous):
        self.predecessors.append(previous)
        print("Succesfully appended ", previous, " to the object")
        
    def append_successor(self, successor):
        self.successors.append(successor)
        print("Succesfully appended ", successor, " to the object")
        
    def append_item(self, item):
        if self.is_cluster:
            self.itself.append(item)
            print("Succesfully appended ", item, " to the object")
        else:
            print("This is not a cluster, there can't be more activities here")
            
    def delSuccesor(self, item):
        del self.successors[item]
        return True
    
    def delPredecessor(self, item):
        print("Deleting: ", item, " from predecessors")
        print("Current predecesors: ", self.get_predecessors())
        self.predecessors.remove(item)
        print("Deletion was succesful")
        return True
    
    def delItem(self, item):
        del self.itself[item]
        return True
    
    def defsignificance(self,unary):
        cnt = 0
        val = 0
        for i in self.get_elements():
            cnt += 1
            val += unary[i]
        self.unarySignificance = val/cnt
        return self.unarySignificance
    
    def getunarySignificance(self):
        return self.unarySignificance
        
                