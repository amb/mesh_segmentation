import random
import bpy
import bmesh

def assignMaterials(mesh, k, idx):
    """Assigns a random colored material for each found segment"""

    # clear all existing materials
    while mesh.materials:
        mesh.materials.pop(0, update_data=True)

    for i in range(k):
        material = bpy.data.materials.new(''.join(['mat', mesh.name, str(i)]))
        material.diffuse_color = (random.random(),
                                  random.random(),
                                  random.random())
        mesh.materials.append(material)

    for i, id in enumerate(idx):
        mesh.polygons[i].material_index = id

def assignUVs(mesh, k, idx):
    """Assigns a UV island for each found segment"""
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(mesh)

    # currently blender needs both layers.  
    uv_layer = bm.loops.layers.uv.verify()
    bm.faces.layers.tex.verify()  

    bm.faces.ensure_lookup_table()

    # create UVs from clusters
    for i, id in enumerate(idx):
        f = bm.faces[i]
        for l in f.loops:
            luv = l[uv_layer]
            luv.uv.x = l.vert.co.x + id * 1.0
            luv.uv.y = l.vert.co.y

    bmesh.update_edit_mesh(mesh)

    bpy.ops.uv.seams_from_islands()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)



