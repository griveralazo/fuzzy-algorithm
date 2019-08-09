# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:36:53 2019

@author: jgonz
"""

import csv

input = open('compras_sap.csv', 'rb')
output = open('comprassap.csv', 'wb')
writer = csv.writer(output)
for row in csv.reader(input):
    if row:
        print(row)
        print('\n')
        writer.writerow(row)
input.close()
output.close()