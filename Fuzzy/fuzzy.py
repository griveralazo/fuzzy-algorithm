# -*- coding: utf-8 -*-
"""
Created on Wed May 15 14:09:59 2019

@author: jgonz
"""
from node import Node
import nltk

class Fuzzy:
    def hola(self):
        print("hola")
        
    def getNodeList(self, heu_net):
        nodesList = list()
        for i in heu_net.dfg:
            nodesList.append(i)
        return nodesList
        
    def relation(self, heu_net, preservethereshold, ratiothereshold):
        unaryCorrelation = self.getunaryCorrelation(heu_net.activities_occurrences)
        #unaryCorrelation = self.delete_noshow(heu_net, unaryCorrelation)
        binarySignificance = self.getBinarySignificance(heu_net, unaryCorrelation, 0.3, 0, 1)
        rel = {}
        nodesList = self.getNodeList(heu_net)
        ##################
        for j in nodesList:
            if (j[1],j[0]) in binarySignificance:
                sum1 = 0
                for k in binarySignificance:
                    if k[0] == j[0]:
                        sum1 += heu_net.dfg[j]
                sum2 = 0
                for k in binarySignificance:
                    if k[1] == j[1]:
                        sum2 += heu_net.dfg[k]
                if sum1 == 0:
                    calc1 = 0
                else:
                    calc1 = ((1/2)*((heu_net.dfg[j])/sum1))
                if sum2 == 0:
                    calc2 = 0
                else:
                    calc2 = ((1/2)*((heu_net.dfg[k])/sum2))
                rel[(j)] = (calc1 + calc2)
        
        new_dfg = {}
        
        
        for j in rel:
            if rel[j]<preservethereshold:
                offset = rel[j]-rel[(j[1],j[0])]
                if offset < 0:
                    offset = -offset
                    lower = 0
                else:
                    lower = 1
                if ((j not in new_dfg) and ((j[1],j[0])not in new_dfg)):
                    if offset >= ratiothereshold:
                        if lower == 0:
                            #j is lower than j1j0
                            new_dfg[j] = (heu_net.dfg[j], 'noshow')
                            new_dfg[(j[1],j[0])] = (heu_net.dfg[(j[1],j[0])], 'show')
                        elif lower == 1:
                            #j1j0 is lower than j
                            new_dfg[j] = (heu_net.dfg[j], 'show')
                            new_dfg[(j[1],j[0])] = (heu_net.dfg[(j[1],j[0])], 'noshow')
                        #remover al que tiene menor significancia relativa
                    elif offset < ratiothereshold:
                        new_dfg[j] = (heu_net.dfg[j], 'noshow')
                        new_dfg[(j[1],j[0])] = (heu_net.dfg[(j[1],j[0])], 'noshow')
                        #remover ambos
        
        for k in heu_net.dfg:
            if k not in new_dfg:
                new_dfg[k] = (heu_net.dfg[k], 'show')
        
        heu_net.new_dfg = new_dfg
        return heu_net
    
    
    def getOwnerCorrelation(self, heuactivities, log):
        activities = {}
        for j in heuactivities:
            print(j)
            count = 0
            newlst = {}
            for index, row in log.iterrows():
                if (row.activity) == j:
                    count += 1
                    if row.resource not in newlst:
                        newlst[row.resource] = 1
                    else:
                        newlst[row.resource] = newlst[row.resource] + 1
            for o in newlst:
                print(o, ' ', newlst[o])
            if count > 0:
                for k in newlst:
                    newlst[k] = newlst[k]/count
                activities[j] = newlst
        return activities
                    
    def getOwnerCorrelationB(self, heuactivities, log, nodeList): #Not sure if I should call nodeList if it's already in the object, but whatever
        activities = self.getOwnerCorrelation(heuactivities, log)
        corr = {}
        for i in nodeList:
            r = max(activities[i[0]].values()) * max(activities[i[1]].values())
            corr[i] = r
        return corr
        
    
    def getWordsCorrelation(self, nodeList):
        corr = {}
        for node in nodeList:
            r = 1 - (nltk.edit_distance(node[0], node[1]) / max(len(node[0]), len(node[1])))
            corr[node] = r
        return corr
    
    
    def getBinarySignificance(self, heu_net, unaryCorrelation, alpha, weightF, weightD):
        print(unaryCorrelation)
        FrequencySignificance = {}
        DistanceSignificance = {}
        maxFrequency = 0
        for i in heu_net.dfg:
            if heu_net.dfg[i] > maxFrequency:
                maxFrequency = heu_net.dfg[i]
        for j in heu_net.dfg:
            if j not in FrequencySignificance:
                FrequencySignificance[j] = heu_net.dfg[j]/maxFrequency
        for k in FrequencySignificance:
            if k not in DistanceSignificance:
                if abs(unaryCorrelation[k[0]] - unaryCorrelation[k[1]]) < alpha:
                    DistanceSignificance[k] = FrequencySignificance[k]*(1-alpha)
                elif abs(unaryCorrelation[k[0]] - unaryCorrelation[k[1]]) > alpha:
                    DistanceSignificance[k] = FrequencySignificance[k]*(1+alpha)
                else:
                    DistanceSignificance[k] = FrequencySignificance[k]
        if weightF == 0 and weightD != 0:
            return DistanceSignificance
        elif weightF != 0 and weightD == 0:
            return FrequencySignificance
    
    def getCorrelations(self, heu_net, nodeList):
        ProximityCorrelationQuantity = {}
        ProximityCorrelationPerformance = {}
        for j in nodeList:
            if j not in ProximityCorrelationQuantity:
                sumproximity = 0
                for k in nodeList:
                    if k[0] == j [0] or k[1] == j[1]:
                        sumproximity += heu_net.dfg[j]
                ProximityCorrelationQuantity[j] = heu_net.dfg[j]/sumproximity
                
            if j not in ProximityCorrelationPerformance:
                sumperformance = 0
                for k in nodeList:
                    if k[0] == j [0] or k[1] == j[1]:
                        sumperformance += heu_net.performance_dfg[j]
                ProximityCorrelationPerformance[j] = heu_net.performance_dfg[j]/sumperformance
        return[ProximityCorrelationQuantity, ProximityCorrelationPerformance]
        
    def fCorrelation(self, ProxCorrelationQ, ProxCorrelationP, OwnerCorrelation, WordsCorrelation):
        fcorr = {}
        for k in ProxCorrelationQ:
            r = (ProxCorrelationQ[k] + ProxCorrelationP[k] + OwnerCorrelation[k] + WordsCorrelation[k])/4 #Average Correlations
            #This is blasphemy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!But I dont care, for now
            fcorr[k] = r
        return fcorr

    def getProximityCorrelation(self, heu_net):
        maxduration = 0
        for j in heu_net.performance_dfg:
            print("$$")
            print(heu_net.performance_dfg[j])
            if heu_net.performance_dfg[j] > maxduration:
                maxduration = heu_net.performance_dfg[j]
        ProximityCorrelation = {}
        for k in heu_net.performance_dfg:
            ProximityCorrelation[k] = heu_net.performance_dfg[k] / maxduration
        return ProximityCorrelation
    
    def fcorr(self, ProxCorrelationQ, ProxCorrelationP, OwnerCorrelation, WordsCorrelation):
        fcorr = {}
        

    def edge_filter(self, heu_net, utilityrt, cutoff, log):
        #Para la correlacion AB, AB /AX
        #For a in dfg
        #crear diccionario con correlaciones de cada uno AB
        #Usar formula
        nodeList = self.getNodeList(heu_net)
        """
        correlations = self.getCorrelations(heu_net, nodeList)
        ProximityCorrelationQuantity =    correlations[0]
        ProximityCorrelationPerformance = correlations[1]
        """
        unaryCorrelation = self.getunaryCorrelation(heu_net.activities_occurrences)
        #unaryCorrelation = self.delete_noshow(heu_net, unaryCorrelation)
        binarySignificance = self.getBinarySignificance(heu_net, unaryCorrelation, 0.3, 0, 1)
        proximityCorrelation = self.getProximityCorrelation(heu_net)
        """
        OwnerCorrelations = self.getOwnerCorrelationB(heu_net.activities, log, nodeList)
        WordCorrelation = self.getWordsCorrelation(nodeList)
        fcorr = self.fCorrelation(ProximityCorrelationQuantity, ProximityCorrelationPerformance, OwnerCorrelations, WordCorrelation)
        """
        #Crear la wea de correlaciones correcta
                
        utility = {}
        #util(A, B) = ur · sig(A, B) + (1 −ur) · cor(A, B)
        #Since the formula uses sig(A,B), we are going to use the quantity correlation, but it can easily be swapped for
        #the performance correlation
        for j in nodeList:
            if j not in utility:
                #utility[j] = (utilityrt * heu_net.dfg[j]) + ((1 - utilityrt) * fcorr[j])
                utility[j] = (utilityrt * binarySignificance[j]) + ((1 - utilityrt) * proximityCorrelation[j])
                #DEBIERA SER utility ry * binary significance + ((1 - utilityrt) * corrJ)
        
        normalizedData = {}
        minutiliy = min(utility, key=utility.get)
        maxutiliy = max(utility, key=utility.get)
        #if minutiliy == maxutiliy we gotta do something else
        
        for k in utility:
            if k not in normalizedData:
                normalizedData[k] = (utility[k]-utility[minutiliy])/(utility[maxutiliy]-utility[minutiliy])
        for j in heu_net.new_dfg:
            if heu_net.new_dfg[j][1] == 'show' and normalizedData[j] < cutoff:
                heu_net.new_dfg[j] = (heu_net.new_dfg[j][0], 'noshow')
        #heu_net.fcorr = fcorr
        return heu_net
    
    def getunaryCorrelation(self, activities_occurrences):
        unaryCorrelation = {}
        maxactivity = 0
        for i in activities_occurrences:
            if (maxactivity < activities_occurrences[i]):
                maxactivity = activities_occurrences[i]
        for j in activities_occurrences:
            unaryCorrelation[j] = activities_occurrences[j]/maxactivity
        return unaryCorrelation
    
    def delete_noshow(self, heu_net, lst):
        for k in list(lst):
            show = False
            for j in heu_net.new_dfg:
                if len(j) == len(k):
                    if j == k:   
                        if heu_net.new_dfg[j][1] == "show":
                            show = True
                else:
                    if j[0] == k or j[1] == k:
                        if heu_net.new_dfg[j][1] == "show":
                            show = True
            if show == False:
                del lst[k]
        return lst
    
    def succesorAndPredecessor(self, correlation, k):
        predecessor = ""
        successor = ""
        for j in correlation:
            if j[1] == k:
                predecessor = j[0]
                
            if j[0] == k:
                successor = j[1]
                
        return [predecessor, successor]
    
    def merge(self, victims, survivors):
        final = []
        v = victims
        for i in list(v):
            controlP = 0
            controlS = 0
            if len(i.get_predecessors()) > 0:
                for j in i.get_predecessors():
                    if j[1] == "S":
                        controlP = 1
            else: 
                controlP = 1
            if len(i.get_successors()) > 0:
                for j in i.get_successors():
                    if j[1] == "S":
                        controlS = 1
            else:
                controlS = 1
            ### If controlP and controlS are 1, then the cluster is ready
            """
            print("predecesors: ",i.get_predecessors())
            print("successors:  ",i.get_successors())
            print("elements:    ",i.get_elements())
            print("Is victim:   ",i.is_cluster())
            print(controlP)
            print("**************************************")
            print()
            """
            while(controlP == 0):
                """
                print("predecesors: ",i.get_predecessors())
                print("successors:  ",i.get_successors())
                print("elements:    ",i.get_elements())
                print("Is victim:   ",i.is_cluster())
                print(controlP)
                print("**************************************")
                print()
                """
                if len(i.get_predecessors()) > 0:
                    for j in i.get_predecessors():
                        if j[1] == "S":
                            controlP = 1
                else: 
                    controlP = 1
                if controlP == 0:
                    for j in list(i.get_predecessors()):
                        #i.append_item(j)
                        for k in v:
#                            print(k.get_elements())
                            if ((j[0] in k.get_elements()) and i != k):
                                if k.is_cluster():
                                    for l in k.get_elements():
                                        i.append_item(l)
                                        
                                    if len(k.get_predecessors()) > 0:
                                        for l in k.get_predecessors():
                                            i.append_predecessor(l)
                                    if len(k.get_successors()) > 0:
                                        for l in k.get_successors():
                                            if l not in i.get_elements():
                                                i.append_Successor(l)
                                    if i in v:
                                        print("i is in v")
                                    else:
                                        print("i is not in v, duh!")
                                        
                                    if i not in v:
                                        v.append(i)
                                        print("appended i")
                                        
                                    print("//////////////////////////////////")
                                    print("We are removing ", k.get_elements())
                                    print()
                                    print("We have ", i.get_elements())
                                    print("//////////////////////////////////")
                                    print("Before removal, we have:")
                                    for x in v:
                                        print("# ", x.get_elements())
                                    v.remove(k)
                                    i.delPredecessor(j)
                                    print("In the list there currenty are:")
                                    for x in v:
                                        print("* ", x.get_elements())
        final = survivors
        for f in v:
            final.append(f)
        return final
                                            
            
            
            
    
    def merge2(self, victims, survivors, heu_net):
        v  = victims
        final = []
        for i in list(v):
            elements = i.get_elements()
            
            unaryCorrelation = self.getunaryCorrelation(heu_net.activities_occurrences)
            
            #node = Node(elements[0], "Cluster", placeholder)
            node = Node(elements[0], "Cluster")
            node.append_predecessor(i.get_predecessors())
            node.append_successor(i.get_successors())
            if len(elements) > 1:
                for k in range(1, len(elements)):
                    node.append_item(elements[k])
            #k is reseted now
            for k in list(v):
                if k.get_elements() != elements:
                    for j in k.get_elements():
                        if j in elements:
                            # if at least one element is is the list
                            for h in k.get_elements():
                                node.append_item(h)
                                if len(k.get_predecessors()) > 0:
                                    for kpredecessor in k.get_predecessors():
                                        print("kpredecessor: ", kpredecessor)
                                        node.append_predecessor(kpredecessor)
                                if len(k.get_successors()) > 0:
                                    for ksuccessor in k.get_successors():
                                        print("ksuccessor: ", ksuccessor)
                                        node.append_successor(ksuccessor)
                            break
                v.remove(k)
            final.append(node)
        return final
                        
    
    def aggregation(self, heu_net, nodeCutoff):
        unaryCorrelation = self.getunaryCorrelation(heu_net.activities_occurrences)
        unaryCorrelation = self.delete_noshow(heu_net, unaryCorrelation)
        
        for k in unaryCorrelation:
            if unaryCorrelation[k] < nodeCutoff:
                unaryCorrelation[k] = (unaryCorrelation[k],"victim") 
            else:
                unaryCorrelation[k] = (unaryCorrelation[k],"survivor") 
        
        survivor = list()
        victims = list()
        
        correlation = self.getProximityCorrelation(heu_net)
        correlation = self.delete_noshow(heu_net, correlation)
        surcount = 0
        for k in unaryCorrelation:
            if unaryCorrelation[k][1] == "survivor":
                surv = Node(k, "survivor", unaryCorrelation[k][0])
                #can a node be important enough to be a survivor but insignificant enough to be deleted in the previous functions?
                
                ret = self.succesorAndPredecessor(correlation, k)
                if len(ret[0]) > 0:
                    surv.append_predecessor(ret[0])
                if len(ret[1]) > 0:
                    surv.append_successor(ret[1])
                survivor.append(surv)
                surcount += 1

            else:
                vict = Node(k, "Cluster", 0)
                corr = -10
                pos = -1
                el = "noValue"
                
                for j in list(correlation):
                    if (j[0] == k or j[1] == k) and correlation[j] > corr:
                        corr = correlation[j]
                        if j[0] == k:
                            el = j[1]
                            pos = 1
                        elif j[1] == k:
                            el = j[0]
                            pos = 0
                        #There has to be a better way to do this!!!!!!!!!!!
                print("el: ", el)
                if el != "noValue":
                    if unaryCorrelation[el][1] == "survivor":
                        if pos == 1:
                            vict.append_successor((el,"S"))
                            del correlation[(k,el)]
                        elif pos == 0:
                            vict.append_predecessor((el,"S"))
                            del correlation[(el,k)]
                    elif unaryCorrelation[el][1] == "victim":
                        #vict.append_item(el)
                        ret = self.succesorAndPredecessor(correlation, k)
                        prevEvent = ret[0]
                        print("prevEvent :", prevEvent, len(prevEvent))
                        if len(prevEvent)>0:
                            print("UCPE: ", unaryCorrelation[prevEvent])
                            if unaryCorrelation[prevEvent][1] == "victim":
                                vict.append_predecessor((prevEvent, "V"))
                                print(vict.get_predecessors())
                            elif unaryCorrelation[prevEvent][1] == "survivor":
                                vict.append_predecessor((prevEvent, "S"))
                                print(vict.get_predecessors())
                            print("++++++++++++++++++++++")
                            print(vict.get_predecessors())
                            print(vict.get_successors())
                            print("++++++++++++++++++++++")
                            
                        nextEvent = ret[1]
                        print("nextEvent: ", nextEvent, len(nextEvent))
                        if len(nextEvent) > 0:
                            if unaryCorrelation[nextEvent] == "victim":
                                vict.append_successor((nextEvent, "V"))
                            elif unaryCorrelation[nextEvent] == "survivor":
                                vict.append_successor((nextEvent, "S"))
                            print(vict.get_predecessors())
                            print(vict.get_successors())
                        
                        """
                        if pos == 1:
                            del correlation[(k,el)]
                        elif pos == 0:
                            del correlation[(el,k)]
                        """
                        """    
                        print(correlation)
                        print(k,el)
                        if pos == 1:
                            del correlation[(k,el)]
                        elif pos == 0:
                            del correlation[(el,k)]
                        """
                    #If el was deleted from unaryCorrelation, then do nothing
                victims.append(vict)
        
        p = self.merge(victims, survivor)
        print("SURCOUNT: ", surcount)
        print("######################################")
        print("######################################")
        print("######################################")
        print()
        print("**************************************")
        print("************Survivors?****************")
        print("**************************************")
        for k in survivor:
            print("predecesors: ",k.get_predecessors())
            print("successors:  ",k.get_successors())
            print("elements:    ",k.get_elements())
            print("Is victim:   ", k.is_cluster())
            print()
        print("**************************************")
        print("**************************************")
        print("************Victims**?****************")
        print("**************************************")
        for k in victims:
            print("predecesors: ",k.get_predecessors())
            print("successors:  ",k.get_successors())
            print("elements:    ",k.get_elements())
            print("Is victim:   ", k.is_cluster())
            print()
        print("**************************************")
        
        
        
        print("****************p*********************")
        for k in p:
            print("predecesors: ",k.get_predecessors())
            print("successors:  ",k.get_successors())
            print("elements:    ",k.get_elements())
            print("Is victim:   ", k.is_cluster())
            print()
        print("**************************************")
        
        return [survivor, victims]
                
                    