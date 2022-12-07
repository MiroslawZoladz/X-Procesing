import os,sys,inspect

def do(nest_degr = 1):
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    
    parentdir = currentdir
    for i in range(nest_degr):
        parentdir = os.path.dirname(parentdir)
    
    sys.path.insert(0,parentdir) 