
import pickle
import os
from con_reader import CONreaderVM

patientPath = r'D:\Egyetem\MSC\2.félév\Projektfeladat\Patient_data'
PatientID = []
files = os.listdir(patientPath)
for ID in files:
    PatientID.append(ID)

# reading the contours
validID = []

for i in range(len(PatientID)):with open(FileName, 'wb') as pck:
            pickle.dump((metafile.read(),contours),pck) #fill up pickle
            pck.close()    #close pickle
    ID=PatientID[i]

    con_file = os.path.join(patientPath,ID,'sa\contours.con')
    meta_file = os.path.join(patientPath,ID,'meta.txt')

    try:
        cr = CONreaderVM(con_file)
        contours = cr.get_hierarchical_contours()
        patientdict=dict()
        #reading the metafile
        metafile = open(meta_file,"r") #open metafile
        FileName='Patient_'+ID+'.pickle' #create pickle file
        with open(FileName, 'wb') as pck:
            pickle.dump((metafile.read(),contours),pck) #fill up pickle
            pck.close()    #close pickle
        validID.append(ID)

    except:
        print('an error occoured while try to access patient data with the ID: ' + ID)

