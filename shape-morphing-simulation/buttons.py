from bge import logic as l 


def main(cont):
    obj=cont.owner
    name=obj.name
    sensors=obj.sensors
    left=sensors['left']
    over=sensors['over']
    
    if(left.positive and over.positive):
      
        l.globalDict['target']=obj.name