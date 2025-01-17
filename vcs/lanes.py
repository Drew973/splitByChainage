# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:27:12 2024

@author: Drew.Bennett

valid patern is : 
    HS
    CL1
    CR1
    
offset from centerline (between CL_N and CR1) depends how many lanes in road.
"""


import re
import numpy as np

from collections import OrderedDict

defaultRoadLanes = OrderedDict([('HS', 3.3), ('CL1', 3.65), ('CL2', 3.65), ('CL3', 3.65)])


def left(lanes,roadLanes = defaultRoadLanes):
    pass
    



lanePattern = re.compile(r'(HS|CL\d+|CR\d+)')



class lanes:
    
    
    
    def __init__(self,data = []):
        self.data = np.unique(np.array(data,dtype = str))
        
    def __str__(self):
        return ','.join(self.data)
        
    
    def names(self):
        return self.data
    
    def __repr__(self):
        return 'lanes:' + str(self.data)
        
    
    #HS then CL then CR
    def leftmost(self):
        if 'HS' in self.data:
            return 'HS'
        return min(self.data)
        
    
    #lanes like CL1. does not include HS
    def CL(self):
        return [a for a in self.data if a[0:2] == 'CL']
    
    #lanes like CR1
    def CR(self):
        return [a for a in self.data if a[0:2] == 'CR']    
    
    
    @staticmethod 
    def fromString(s):
        r = lanes()
        r.data = lanePattern.findall(s)#[str]
        return r
    
        
    #str. '' for valid.
    def invalidRoad(self):
        cl = self.CL()
        if len(cl) == 0:
            return 'No CL lanes'
        
        if min(cl) != 'CL1':
            return 'CL lanes do not start at 1'
        
        cr = self.CR()
        if cr:
            if min(cr) != 'CR1':
                return 'CR lanes do not start at 1'
            
        return ''
    
    
    #offset of left hand side. Centerline between CL and CR. Result depends on number of lanes in road.
    # +ve         HS,CL1,CL2,CLN     centerline/0    CR1,CR2,CRN    -ve

    def leftOffset(self , roadLanes , laneWidth = 3.65 , HSWidth = 3.3):
        lm = self.leftmost()
    
        if lm == 'HS':
            return HSWidth + laneWidth * len(roadLanes.CL())
    
        if lm[0:2] == 'CL':
            d = sorted(roadLanes.CL())
            i = d.index(lm)
            c = len(d) - i
            return laneWidth * c
    
        if lm[0:2] == 'CR':
            d = sorted(roadLanes.CR())
            return - laneWidth * d.index(lm)    
    
    
    @staticmethod
    def roadEdges(roadLanes):
        return [lanes.fromString(s).leftOffset(roadLanes = roadLanes) for s in roadLanes.names()] + [0.0]

    
    #'bitwise' or
    def __or__(self,other):
        return lanes(data = np.append(self.data,other.data))
        
    
    @staticmethod
    def overlap(a,b):
        return lanes(data = [d for d in a.data if d in b.data])
            
        
        
    
def testLanesFromString():
  #  s = 'CL1,CL2,HS'
 #   s = 'CL1,CL2'
    s = 'CR1,CL1'

    r = lanes.fromString(s)
    print(r)
    print(r.leftmost())
    
    rl = lanes.fromString('CL1,CR1')
    print('rl',rl)
    lo = r.leftOffset(rl)
    print('leftOffset',lo)
    
   # print('addition',r + rl)
    
if __name__ in ('__main__','__console__'):
    testLanesFromString()    
    
    
    