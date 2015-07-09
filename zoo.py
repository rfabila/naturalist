import os
import PyDCG
import pickle

eval_functions={'rectilinear_crossing_number':PyDCG.crossing.count_crossings,
                'empty_convex_pentagons':PyDCG.holes.count_convex_rholes_maker(5),
                'empty_triangles':PyDCG.holes.countEmptyTriangs,
                'empty_convex_quadrilaterals':PyDCG.holes.count_convex_rholes_maker(4),
                'empty_convex_hexagon':PyDCG.holes.count_convex_rholes_maker(6)}

#Whether it is a minimize or maximizing species
min_species={'rectilinear_crossing_number':True,
                'empty_convex_pentagons':True,
                'empty_triangles':True,
                'empty_convex_quadrilaterals':True,
                'empty_convex_hexagon':True}

genus=[['rectilinear_crossing_number'],['empty_convex_pentagons','empty_triangles',
                                        'empty_convex_quadrilaterals',
                                        'empty_convex_hexagon']]

#suscriber functions
def to_oswin(sp,species):
    pass

suscribers={2:to_oswin}

def full_update():
    Original_zoo=get_zoo()
    Z=get_zoo()
    sp_list=get_new_sp_list()
    for (sp,species) in sp_list:
        update_sp(sp,species,Z)
    D=compare_zoos(Z1,Z2)
    #mail diffs

def compare_zoos(Z1,Z2):
    species_list=get_species_list()
    Diffs={}
    for species in species_list:
        Diffs[species]=0
        for k in Z2[species]:
            if (k not in Z1[species] or Z2[species][k]['val']!=Z1[species][k]['val']):
                Diffs[species]+=1
    return Diffs

def clean_submissions(file_list):
    for name in file_list:
        os.system("rm captured_specimens/"+name)

def get_filelist():
    file_list=os.listdir("captured_specimens/")
    return file_list

def get_new_sp_list():
    lst=[]
    file_list=get_filelist()
    for name in file_list:
        file_sp=open("captured_speciments/"+name,"r")
        species_sp=pickle.load(file_sp)
        file_sp.close()
        lst.append(species_sp)
    return lst

def update_sp(sp,species,Z):
    user=sp['user']
    for i in range(len(genus)):
        if species in genus[i]:
            gen=genus[i]
    for species in gen:
        if new_specimen(sp,species,Z):
            for p in suscribers:
                if p!=user:
                    suscribers[p](sp,species)

def get_species_list():
    lst=[]
    file_species=open("species.txt","r")
    for species in file_species:
        lst.append(species.strip())
    file_species.close()
    return lst

def get_zoo():
    Z={}
    species_lst=get_species_list()
    for species in species_lst:
        file_sp=open("../PyDCG/PyDCG/point_sets/"+species+".pkl","r")
        Z[species]=pickle.load(file_sp)
        file_sp.close()
    return Z

def save(species):
    file_sp=open("../PyDCG/PyDCG/point_sets/"+species+".pkl","w")
    pickle.dump(Z[species],file_sp)
    file_sp.close()

def new_specimen(sp,species,Z):
    pts=sp["pts"]
    n=len(pts)
    if not PyDCG.geometricbasics.general_position(pts):
        False
    new_val=eval_functions[species](pts)
    old_val=Z[species][n]['val']
    if new_val<old_val and min_species[species]:
       Z[species][n]=sp
       save(species)
       return True
    if new_val>old_val and not min_species[species]:
       Z[species][n]=sp
       save(species)
       return True
    return False






