
import os
import re

class ParseOBJ:

    nodal_coordinates=[]
    texture_coordinates=[]
    element_normals=[]
    element_indices=[]

    def Parse(self,filepath):
        self.nodal_coordinates.clear()
        self.texture_coordinates.clear()
        self.element_normals.clear()
        self.element_indices.clear()
        file = self.OpenFile(filepath)
        self.ParseOBJ(file)


    def OpenFile(self,filepath):
        current_directory = os.getcwd()
        print(current_directory)
        source = current_directory + '\\' + filepath
        file = open(source, 'r')
        return file

    def ParseNodalCoordinates(self,file):
        anyVertexes = False
        
        while(file.readable()):
            line = file.readline()
            line = line.split(' ')
            vertex = []
            if(line[0] == 'v'):
                for i in range(1,len(line)):
                    vertex.append(float(line[i]))
                    anyVertexes = True
                self.nodal_coordinates.append(vertex)
            elif(anyVertexes == True):
                return anyVertexes
            
    def ParseTextureCoordinates(self,file):
        anyVT = False
        while(file.readable()):
            line = file.readline()
            line = line.split(' ')
            vertex = []
            if(line[0] == 'vt'):
                for i in range(1,len(line)):
                    vertex.append(float(line[i]))
                    anyVT = True
                self.texture_coordinates.append(vertex)
            elif(anyVT):
                return anyVT
            
    def ParseElementNormals(self,file):
        anyVT = False
        while(file.readable()):
            line = file.readline()
            line = line.split(' ')
            vertex = []
            if(line[0] == 'vn'):
                for i in range(1,len(line)):
                    vertex.append(float(line[i]))
                    anyVT = True
                self.element_normals.append(vertex)
            elif(anyVT):
                return anyVT
            
    def ParseElementIndices(self,file):
        anyVT = False
        while(file.readable()):
            line = file.readline()
            line = line.split(' ')
            vertex = []
            if(line[0] == 'f'):
                for i in range(1,len(line)):
                    vertex.append(line[i])
                    anyVT = True
                self.element_indices.append(vertex)
            elif(anyVT):
                return anyVT
        
    def ParseOBJ(self,fileX):
        verticesPresent = self.ParseNodalCoordinates(fileX)
        if(verticesPresent == False):
            fileX.close()
            return False
        self.ParseTextureCoordinates(fileX)
        normalsPresent = self.ParseElementNormals(fileX)
        if(normalsPresent == False):
            fileX.close()
            return False
        indicesPresent = self.ParseElementIndices(fileX)   
        if(indicesPresent == False):
            fileX.close()
            return False


class OBJToFEA:
    element_type = 'quadrilateral'
    number_of_nodes = 0
    nodes_per_element = 0
    number_of_elements = 0
    number_of_integrating_points = 0
    number_of_dimensions = 0
    number_of_property_types = 0

    property_matrix = []
    element_types = []
    nodal_coordinates = []
    nodal_numbers = []

    ParsedOBJ = 0

    def __init__(self,obj):
        self.ParsedOBJ = obj
        self.parseFromOBJ()
    
    def fillNodalCoordinates(self):
        num_nodal_faces = self.number_of_elements

        for i in range(0, num_nodal_faces):
            face_vector = self.ParsedOBJ.element_indices[i]
            for j in range(0,len(face_vector)):
                face_vector[j].replace('\n','')
                face_string = face_vector[j].split('/')
                vertex_index = int(face_string[0])
                self.nodal_numbers.append(vertex_index)
                self.nodal_coordinates.append(self.ParsedOBJ.nodal_coordinates[vertex_index-1])


    def parseFromOBJ(self):
        #nodal_coordinates=[]
        #texture_coordinates=[]
        #element_normals=[]
        #element_indices=[]
        
        self.number_of_nodes = len(self.ParsedOBJ.nodal_coordinates)
        self.nodes_per_element = 4
        self.number_of_elements = len(self.ParsedOBJ.element_indices)
        self.number_of_integrating_points = 4
        self.number_of_dimensions = 3
        self.number_of_property_types = 2 

        #how to define property types


        self.fillNodalCoordinates()



        #self.property_matrix = 
        #self.element_types = 
        #self.nodal_coordinates = 
        #self.nodal_numbers = 



                 
Obj = ParseOBJ()       
Obj.Parse("meshes\\carhood.obj")
OBJToFEA(Obj)           


    



