from random import random
from cymesh.mesh import Mesh
from cymesh.view import Viewer

mesh = Mesh.from_obj('triangulated_sphere_2.obj')

# Add noise to mesh.
for vert in mesh.verts:
    vert.p[0] += random() * .2
    vert.p[1] += random() * .2
    vert.p[2] += random() * .2

# If not given a max length, all edges are split.
mesh.splitEdges()

# Flip edges which will become shorter.
mesh.shortenEdges()

# Normals and curvature updates must be called after making changes to mesh.
mesh.calculateNormals()
mesh.calculateCurvature()

# We can write our new object to a file.
mesh.writeObj('my_mesh.obj')

# We can also export the mesh to a dict of numpy arrays.
export = mesh.export()
print(export.keys())
# > dict_keys(['faces', 'vertice_normals', 'face_normals', 'vert_data', 'vertices', 'curvature', 'edges'])

# Each vert has a dictionary 'data' attribute to add additional information.
# Colors can be passed to the viewer by adding a color to data.
for vert in mesh.verts:
    if vert.curvature > 0:
        vert.data['color'] = (2*vert.curvature, 0.0, 0.0)
    else:
        vert.data['color'] = (0.0, -2 * vert.curvature, 0.0)

# View the mesh with pyopengl.
view = Viewer()
view.startDraw()
view.drawMesh(mesh, edges=False)
view.endDraw()
view.mainLoop()
