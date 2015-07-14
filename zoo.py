import os
import PyDCG
import pickle
import ConfigParser
import smtplib
from email.mime.text import MIMEText


eval_functions={'rectilinear_crossing_number':PyDCG.crossing.count_crossings,
                'empty_convex_pentagons':PyDCG.holes.count_convex_rholes_maker(5),
                'empty_triangles':PyDCG.holes.countEmptyTriangs,
                'empty_convex_quadrilaterals':PyDCG.holes.count_convex_rholes_maker(4),
                'empty_convex_hexagons':PyDCG.holes.count_convex_rholes_maker(6)}

#Whether it is a minimize or maximizing species
min_species={'rectilinear_crossing_number':True,
                'empty_convex_pentagons':True,
                'empty_triangles':True,
                'empty_convex_quadrilaterals':True,
                'empty_convex_hexagons':True}

genus=[['rectilinear_crossing_number'],['empty_convex_pentagons','empty_triangles',
                                        'empty_convex_quadrilaterals',
                                        'empty_convex_hexagons']]

#mail functions.
def mail_all(D):
    U=get_users()
    for user in U:
        user_name=U[user]['user_name']
        mail=U[user]['email']
        msg=create_msg(D,user_name=user_name,email=email)
        if user_name=="Ruy":
            s=smtplib.SMTP("monk")
            s.sendmail("naturalist@monk.math.cinvestav.mx",email,msg.as_string())
            s.quit()
            
        
#User functions
def get_users():
    U={}
    config=ConfigParser.RawConfigParser()
    config.read('users.cfg')
    users=config.sections()
    for u in users:
        U[u]={'user_name':config.get(u,'user_name'),
              'email':config.get(u,'email')}
    return U
        
#message functions
def create_msg(D,user_name="Ruy",email="ruyfabila@gmail.com"):
    file_msg=open("summary_message.txt","r")
    summary=diffs_to_string(D)
    msg_text=file_msg.read()
    msg_text=msg_text.replace('$NAME',user_name)
    msg_text=msg_text.replace('$SUMMARY',summary)
    file_msg.close()
    msg=MIMEText(msg_text)
    
    msg['Subject']="Today's Catch"
    msg['From']="naturalist@monk.math.cinvestav.mx"
    msg['To']=email
    
    return msg
    
    
def diffs_to_string(D):
    s=""
    for species in D:
        s=s+"new "+str(D[species])+" sets for "+species+".\n"
    return s
    
#suscriber functions
def to_oswin(sp,species):
    pass

suscribers={2:to_oswin}

def full_update(mail_summaries=False):
    Z1=get_zoo()
    Z2=get_zoo()
    sp_list=get_new_sp_list()
    for (species,sp) in sp_list:
        update_sp(sp,species,Z2)
    D=compare_zoos(Z1,Z2)
    update_suscribers(Z1,Z2)
    
    if mail_summaries:
        new_sets=False
        species_list=get_species_list()
        for species in species_list:
            if D[species]>0:
                new_sets=True
        if new_sets:
            mail_all(D)

def update_suscribers(Z1,Z2):
    species_list=get_species_list()
    for species in species_list:
        for k in Z2[species]:
             if (k not in Z1[species] or Z2[species][k]['val']!=Z1[species][k]['val']):
                user=Z2[species][k]['user_id']
                for sus in suscribers:
                    if sus!=user:
                        suscribers[sus](Z2[species][k],species)
            

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
        file_sp=open("captured_specimens/"+name,"r")
        species_sp=pickle.load(file_sp)
        file_sp.close()
        lst.append(species_sp)
    return lst

def update_sp(sp,species,Z):
    user=sp['user_id']
    for i in range(len(genus)):
        if species in genus[i]:
            gen=genus[i]
    for species in gen:
        new_specimen(sp,species,Z)
            

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

def save(Z,species):
    file_sp=open("../PyDCG/PyDCG/point_sets/"+species+".pkl","w")
    pickle.dump(Z[species],file_sp)
    file_sp.close()

def new_specimen(sp,species,Z):
    pts=sp["pts"]
    n=len(pts)
    if not PyDCG.geometricbasics.general_position(pts):
        False
    new_val=eval_functions[species](pts)
    if n not in Z[species]:
        Z[species][n]=sp
        sp['val']=new_val
        save(Z,species)
        print "New specimen of "+species+" found!"
        return True
        
    old_val=Z[species][n]['val']
    if new_val<old_val and min_species[species]:
        Z[species][n]=sp
        sp['val']=new_val
        save(species)
        print "New specimen of "+species+" found!"
        return True
    if new_val>old_val and not min_species[species]:
        Z[species][n]=sp
        sp['val']=new_val
        save(species)
        print "New specimen of "+species+" found!"
        return True
    return False






