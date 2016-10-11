# Filename: l-system_tree.py
# Author:   Benjamin N. Summerton (@def-pri-pub)
# License:  See the file `./LICENSE`.
#
# This script is the logic for generating a Lindenmayer System tree.  It's
# needs to be run inside of Blender for it to work.  When it's done genrating
# you should be given a tree-like structure made out of cylinders and spheres


import math
import random
import bpy
from mathutils import Vector, Matrix


### Configuration Options ##

# Tree Characteristics
ANGLE = 45                      # Angle which new branches come off of (in degrees)
BRANCH_LENGTH = 10              # Length of parent branch
BRANCH_DIVISOR = 1.6            # How much to divide parent branch length by
THICKNESS = 0.25                # How thick the branches should be
DEPTH = 5                       # How many levels to render
SOFT_ENDS = True                # Add soft ends (spheres) to the branches

# Twist at the A grammar
TWIST = False                   # Twist the child branches around the parent branch
TWIST_AMOUNT = 45               # How much to twist by

# Mesh Resolution
VERTICES = 16                   # For branches (cylinders)
RING_COUNT = 16                 # For soft ends (spheres)
SEGMENTS = 16                   # For soft ends (spheres)

# Apply some randomness to the tree
VARIATION_MODE = False          # apply a random variation to the tree, gives it a more natural feel
BRANCH_LENGTH_VARIATION = .5    # How much to vary the branch length
TWIST_VARIATION = 15            # How much to vary the twist by
ANGLE_VARIATION = 30            # How much to vary the child branche's branch angle by
#random.seed(0)                 # use this to set a random seed


# class for storing render state
class RenderParams:
    __slots__ = (
        'max_depth',
        'cur_depth',
        'branch_length',
        'matrix_chain',
    )

    # sets up the Rendering Parameters
    def __init__(self, branch_length=10, max_depth=5):
        self.max_depth = max_depth
        self.cur_depth = 0

        self.branch_length = branch_length

        self.matrix_chain = [Matrix.Identity(4)]


    # Checks if we are deeper than our current depth or not
    def depthGood(self):
        return self.cur_depth < self.max_depth

    
    # Multiplies the stored matrx_chain
    def computedMatrixChain(self):
        m = self.matrix_chain[0]
    
        for i in range(1, len(self.matrix_chain)):
            m *= self.matrix_chain[i]
    
        return m


# This is used so that we don't accidentally add more sphere than we need to
_soft_ends_set = set()


# Makes a branch
#   branch_length -- a non-negative number, how long each branch should be
#   world_matrix -- A Matrix that will be where the placement of the branch starts
def mkBranch(branch_length, world_matrix):
    global _soft_ends_set

    # For the endpoints
    if SOFT_ENDS:
        # compute locations
        a = world_matrix
        b = world_matrix * Matrix.Translation((0, 0, branch_length))

        # Get their tranlations (fronzen) (so we don't double add them)
        a_loc = a.to_translation().freeze()
        b_loc = b.to_translation().freeze()

        # first endpoint
        if a_loc not in _soft_ends_set:
            _soft_ends_set.add(a_loc)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=SEGMENTS, ring_count=RING_COUNT, size=THICKNESS)
            bpy.context.active_object.matrix_world *= a

        # second
        if b_loc not in _soft_ends_set:
            _soft_ends_set.add(b_loc)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=SEGMENTS, ring_count=RING_COUNT, size=THICKNESS)
            bpy.context.active_object.matrix_world *= b

    # The actual branch
    mid = world_matrix * Matrix.Translation((0, 0, branch_length / 2))
    cylinder = bpy.ops.mesh.primitive_cylinder_add(
        vertices=VERTICES,
        radius=THICKNESS,
        depth=branch_length,
    )
    bpy.context.active_object.matrix_world *= mid


# Grammar
# A -> BCDE
# B -> A
# C -> A
# D -> A
# E -> A

# (All these are in the context of having a max render depth
# A = Go forward x units, perform B & C,  then back x units
# B = Turn left 45 degrees, perform A, then turn right 45 degrees
# C = Turn right 45 degrees, perform A, then turn left 45 degrees


# A - BCDE
def A(rp):
    # Check depth
    if not rp.depthGood():
        return

    # Record the amounts
    original_branch_length = rp.branch_length
    branch_length = rp.branch_length
    twist_amount = TWIST_AMOUNT

    # If variations are on, apply some
    if VARIATION_MODE:
        branch_length += random.uniform(-BRANCH_LENGTH_VARIATION, BRANCH_LENGTH_VARIATION)
        twist_amount += random.uniform(-TWIST_VARIATION, TWIST_VARIATION)

    # Make the branch
    mkBranch(branch_length, rp.computedMatrixChain())

    # Increase distance & twist
    rp.matrix_chain.append(Matrix.Translation((0, 0, branch_length)))
    if TWIST:
        rp.matrix_chain.append(Matrix.Rotation(math.radians(twist_amount), 4, 'Z'))
    rp.branch_length = branch_length / BRANCH_DIVISOR

    # Do the other grammars
    rp.cur_depth += 1
    B(rp)
    C(rp)
    D(rp)
    E(rp)
    rp.cur_depth -= 1

    # undo distance increase and twist
    rp.branch_length = original_branch_length
    if TWIST:
        rp.matrix_chain.pop()
    rp.matrix_chain.pop()


# B -> A
def B(rp):
    # Check depth
    if not rp.depthGood():
        return
    
    # Set the angle
    angle = ANGLE
    if VARIATION_MODE:
        angle += random.uniform(-ANGLE_VARIATION, ANGLE_VARIATION)

    # Rotate & go deeper
    rp.matrix_chain.append(Matrix.Rotation(math.radians(angle), 4, 'X'))
    A(rp)
    rp.matrix_chain.pop()


# C -> A
def C(rp):
    # Check depth
    if not rp.depthGood():
        return
    
    # Set the angle
    angle = ANGLE
    if VARIATION_MODE:
        angle += random.uniform(-ANGLE_VARIATION, ANGLE_VARIATION)

    # Rotate & go deeper
    rp.matrix_chain.append(Matrix.Rotation(math.radians(angle), 4, 'Y'))
    A(rp)
    rp.matrix_chain.pop()


# D -> A
def D(rp):
    # check depth
    if not rp.depthGood():
        return
    
    # Set the angle
    angle = ANGLE
    if VARIATION_MODE:
        angle += random.uniform(-ANGLE_VARIATION, ANGLE_VARIATION)

    # Rotate & go deeper
    rp.matrix_chain.append(Matrix.Rotation(math.radians(-angle), 4, 'X'))
    A(rp)
    rp.matrix_chain.pop()


# E -> A
def E(rp):
    # check depth
    if not rp.depthGood():
        return
    
    # Set the angle
    angle = ANGLE
    if VARIATION_MODE:
        angle += random.uniform(-ANGLE_VARIATION, ANGLE_VARIATION)

    # Rotate & go deeper
    rp.matrix_chain.append(Matrix.Rotation(math.radians(-angle), 4, 'Y'))
    A(rp)
    rp.matrix_chain.pop()


# render something
rp = RenderParams(BRANCH_LENGTH, DEPTH)
A(rp)

