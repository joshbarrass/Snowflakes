##Line storing module

#Idea behind this is to create an effective way of storing things like binary trees

import sys, gc
import numpy

class BranchMap(object):
    class Coordinate(object):
        def __init__(self,coord,death_msg=False):
            self.coord = coord
            self.branches = []
            self.death_msg = death_msg

        def __repr__(self):
            return "Coordinate("+str(self.coord)+", "+str(len(self.branches))+" branches)"

        def raw(self):
            return self.coord

        def __del__(self):
            if self.death_msg:
                print self.__repr__()+" going down!"

        def transform(self,matrix):
            here = numpy.array([[self.coord[0]],[self.coord[1]]])
            here = numpy.dot(matrix,here)
            self.coord = (here.tolist()[0][0],here.tolist()[1][0])

    def transform(self,matrix):
        for c in self.map:
            c.transform(matrix)
        self.update_raw()

    def update_raw(self):
        self.raw_map = [c.coord for c in self.map]
        
    def __init__(self,start_pos,debug=False):
        self.debug = debug
        self.map = [self.Coordinate(start_pos,debug)]
        self.update_raw()
        self.current_coordinate = self.map[0]
        
    def __iter__(self):
        for c in self.map:
            yield (c.coord,[d.coord for d in c.branches])

    def __len__(self):
        return len(self.map)

    class BranchError(Exception):
        pass

    def select_coordinate(self,coord):
        if coord in self.raw_map:
            self.current_coordinate = self.map[self.raw_map.index(coord)]
        else:
            raise self.BranchError("Coordinate '"+str(coord)+"' does not exist in this map.")

    def add_branch(self,coord):
        #self.map[self.current_coordinate].append(coord)
        if coord in self.raw_map:
            self.current_coordinate.branches.append(self.map[self.raw_map.index(coord)])
        else:
            temp = self.Coordinate(coord,self.debug)
            self.current_coordinate.branches.append(temp)
            self.map.append(temp)
            self.update_raw()

    def remove_branch(self,coord):
        raw = [c.raw() for c in self.current_coordinate.branches]
        if coord not in raw:
            raise self.BranchError("Coordinate '"+str(coord)+"' does not branch from this coordinate.")
        else:
            self.current_coordinate.branches.pop(raw.index(coord))
            
    def remove_coordinate(self,coord):
        IGNORE = [locals(),globals(),gc.garbage]
        if coord not in self.raw_map:
            raise self.BranchError("Coordinate '"+str(coord)+"' does not exist in this map.")
        else:
            obj = self.map[self.raw_map.index(coord)]
            self.map.pop(self.raw_map.index(coord))
            self.update_raw()
            for ref in [r for r in gc.get_referrers(obj) if r not in IGNORE]:
                #print ref
                if isinstance(ref,self.Coordinate):
                    ref.branches.remove(obj)
                    #print ref
                if isinstance(ref,list):
                    ref.remove(obj)
                    #print ref
            obj = None
            gc.collect()
            
