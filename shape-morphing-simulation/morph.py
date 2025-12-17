

#lets import some useful modules
from bge import render
from mathutils import Vector as vec
from mathutils import geometry as geo
from bge import logic
from mathutils import Matrix as matr
from itertools import combinations as comb
from threading import Thread as thr
import time
#function to get global position of a vertex on an object
def getGlobal(vert,obj):
    #create matrix transform for the scale
    scale=matr.Translation(vec((0,0,0)))
    for i in range(len(obj.worldScale)):
        #populate the scale matrix with information
        #on th world scale of the object
        scale[i][i]=obj.worldScale[i]
    #create matrix transform to translate the vertex
    #by the object position
    translation=matr.Translation(obj.worldPosition)
    #lets create vertex orientation transform matrix
    #relative to the object world orientatiojn
    rotation=obj.worldOrientation.copy()
    rotation.resize_4x4()
    #compute the global position of the vertex
    pos=translation*rotation*scale*vert
    return pos

#function to get all vertices on an objet
def getVertices(obj):
    mesh=obj.meshes[0]
    vertices=[]
    for mat in range(mesh.numMaterials):
        for v in range(mesh.getVertexArrayLength(mat)):
                   vertices.append(mesh.getVertex(mat,v))
    return vertices

def filterVerts(verts):
    data={}
    data2={}
    copy=[]
    for v in verts:
        c=v.XYZ.copy()
        c.freeze()
        if(v.XYZ not in copy):
            copy.append(v.XYZ)
            
            data[c]=[v]
            data2[c]=[c]
        else:
            data[c].append(v)
    del copy
   
    return data,data2

def locateVertex(center,verts,data,source,target):
   global frac
   if(len(verts)>0):
    vert=verts[0]
    vert2=data[0]
    dir=(vert2.XYZ-center)
    dir_n=dir.normalized()
    farpoint=dir_n*1000
    hitobj,hitp,normal=source.rayCast(vert2.XYZ,farpoint,1000,target,0,1,0)
    for v in data:
        if(hitp!=None):
            
            v.XYZ=frac*(hitp-vert)+vert
            
            v.setNormal(dir)
    return hitp
global prev,frac,center,verts,values,source,target
target='cube'    
cont=logic.getCurrentController()
obj=cont.owner
scene=obj.scene
source=scene.objects['main_object']
center=source.position
verts=getVertices(source)
data,verts=filterVerts(verts)
values=list(data.values())
verts=verts.values()

frac=0
prev=None
print('done')
def main(cont):
    global prev,frac,center,verts,values,source,target
    index=0
    if(logic.globalDict.__contains__('target')):
        gvar=logic.globalDict['target']
        if(gvar!=target):
            target=gvar
            frac=0
            verts=getVertices(source)
            data,verts=filterVerts(verts)
            values=list(data.values())
            verts=verts.values()
    
    for v in verts:
        prev_hit=locateVertex(center,v,values[index],obj,target)
        index+=1
   
    
    if(frac<1.0):
       frac+=0.05
