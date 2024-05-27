import numpy as np
import sympy
import sys
import os
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from state.state import *
from shaders.PyGLHelper import *

s_1 = np.linspace(0,1,200)

def parse_kap_expr(expr):

    arg_array = ['','']
    expr_array = []

    index = 1
    expr_index = 0

    previously_integer = False

    operators = {'*', '/', '+', '-', ' '}

    for i in range(1,len(expr)):
        if(expr[i] == ","):
            expr_index+=1
        elif(expr[i] == ">"):
            break
        else:
            if(previously_integer == True and not expr[i].isnumeric() and expr[i] not in operators):
                arg_array[expr_index]+="*"
            

            arg_array[expr_index]+=expr[i]

            if(expr[i].isnumeric()):
                previously_integer = True
            else:
                previously_integer = False
            

    
    for i in range(0, len(arg_array)):

        expr_array.append( parse_expr(arg_array[i], evaluate=False) )
    

    return expr_array

def kap(expr,t,s):

    expressions = parse_kap_expr(expr)

    return (expressions[0].subs({"t":t}), expressions[1].subs({"s":s}))


def generate_kap_mesh(expr, s_1):
    
    vertex_array = glGenVertexArrays()
    vertex_buffer = glGenBuffers()
    element_buffer = glGenBuffers()

    vertex_index = 0
    element_index = 0

    vertex_data = np.Array([], dtype=np.float32)
    element_data = np.Array([], dtype=np.uint16)
    
    elements = []

    for i in range(0,len(s_1)):
        for j in range(0, len(s_1)):
            print(kap("<3t,4s>", s_1[i], s_1[j]))