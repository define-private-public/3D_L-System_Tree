# Filename: l-system_tree.py
# Author:   Benjamin N. Summerton (@def-pri-pub)
# License:  BSD 3-Clause (read `./LICENSE` for details)
#
# This script is the logic for generating a Lindenmayer System tree.  It's
# needs to be run inside of Blender for it to work.  When it's done genrating
# you should be given a tree-like structure made out of cylinders and spheres


import bpy
import numpy as np 
import random
import mathutils
import math

from mathutils import Vector, Matrix


VERTICES = 6
THICKNESS = 0.2
branch_length = 3
max_depth = 3

ANGLE = 45

VARIATION_MODE = False 
ANGLE_VARIATION = 10

DEC_RATIO = 0.5


class FractalRender:
    def __init__(self, branch_length=10, max_depth=5):
        self.max_depth = max_depth
        self.cur_depth = 0
        
        self.branch_length = branch_length
        
        self.matrix_chain = [Matrix.Identity(4)]
        
        
    def computeMatrixChain(self):
        m = self.matrix_chain[0]
        
        for i in range(1, len(self.matrix_chain)):
            m = m @ self.matrix_chain[i]

        return m


def mkBranch(branch_length, world_matrix):
    mid = world_matrix @ Matrix.Translation((0, 0, branch_length * 0.5))
    
    cylinder = bpy.ops.mesh.primitive_cylinder_add(
        vertices = VERTICES,
        radius = THICKNESS,
        depth=branch_length
    )
    
    bpy.context.active_object.matrix_world = bpy.context.active_object.matrix_world @ mid
    

def fractal(n_iter, fr):
    
    matrix = mkBranch(fr.branch_length, fr.computeMatrixChain())
    
    if n_iter == 0:
        return
    
    for i in [-1, 1]:
        for axis in ['X', 'Y']:
            angle = ANGLE
            
            if VARIATION_MODE:
                angle += random.uniform(-ANGLE_VARIATION, ANGLE_VARIATION)

            rotation_matrix = Matrix.Rotation(math.radians(i * angle), 4, axis)

            vec = Vector((0, 0, fr.branch_length))

            fr.matrix_chain.append(Matrix.Translation(vec))
            fr.matrix_chain.append(rotation_matrix)

            fr.branch_length *= DEC_RATIO
            fractal(n_iter - 1, fr)
            fr.branch_length /= DEC_RATIO

            fr.matrix_chain.pop()
            fr.matrix_chain.pop()


fr = FractalRender()

    
fractal(4, fr)
    
    

