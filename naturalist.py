from pymongo import MongoClient
import pickle
import PyDCG
import fractions

client = MongoClient()
db = client.naturalist

complete_graph = db.complete_graph

def migrate_pts_complete_graph(Q):
    """Migrates an old point set into the database"""
    P={}
    
    for x in Q:
        P[x]=Q[x]
        
    if 'val'not in P:
        cr = PyDCG.crossing.count_crossings(P["pts"])
        P['val']=str(cr)
    else:
        P['val']=str(P['val'])
    
    P["num_pts"]=len(P["pts"])
    ptss=pickle.dumps(P["pts"])
    P["pts"]=ptss
    
    complete_graph.insert_one(P)
    
def migrate_all_cr():
    #THIS IS A LOCAL FUNCTION; DO NOT INCLUDE IT IN THE FINAL VERSION
    file_pts=open("rectilinear_crossing_number.pkl","r")
    P=pickle.load(file_pts)
    for x in P:
        migrate_pts_complete_graph(P[x])

def best_complete_graph(n):
    return complete_graph.find_one({"num_pts":n})

def best_complete_graph_pts(n):
    P=complete_graph.find_one({"num_pts":n})
    if P!=None:
        pts=pickle.loads(P["pts"])
        return pts
    
def all_vals():
    """Returns a list of all (cr,n) where cr is the
    number of crossings and n is the number of points"""
    L=[]
    P=complete_graph.find({"num_pts":{"$gt":4}},{"num_pts":1,"val":1})
    for x in P:
        L.append([x["num_pts"],x["val"]])
    return L

def best_crossing_constant():
    """Returns a tuple (c,n) where c is the best crossing constant
    and n is the size of the size of the point set achieving
    this constant. The constant is returned as a fraction."""
    L=all_vals()
    L=[[crossing_constant(int(x[0]),int(x[1])),int(x[0])] for x in L]
    return min(L)

def crossing_constant(m,cr):
    """Computes the obtained constant with a point set of
       size n and cr crossings. The constant is returned as a fraction"""
    return (24*cr+3*m**3-7*m**2+fractions.Fraction(30,7)*m)/m**4