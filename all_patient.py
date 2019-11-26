# Reads the sa folder wiht dicom files and contours
# then draws the contours on the images.
import math
import pickle
import os
from con_reader import CONreaderVM
from dicom_reader import DCMreaderVM
from con2img import draw_contourmtcs2image as draw

patientPath = r'D:\Egyetem\MSC\2.félév\Projektfeladat\Patient_data'
PatientID = []
files = os.listdir(patientPath)
for ID in files:
    PatientID.append(ID)

# reading the contours
validID = []

for i in range(len(PatientID)):
    ID=PatientID[i]

    con_file = os.path.join(r'D:\Egyetem\MSC\2.félév\Projektfeladat\Patient_data',ID,'sa\contours.con')
    meta_file = os.path.join(r'D:\Egyetem\MSC\2.félév\Projektfeladat\Patient_data',ID,'meta.txt')

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

for x in range(len(validID)):
    pickle_in = open('Patient_'+validID[x]+'.pickle',"rb")
    patient = pickle.load(pickle_in) #run out of input
    metadata = patient[0]
    contours = patient [1]

    # drawing the contours for the images
    for slc in contours:
        for frm in contours[slc]:

            lpLenght=0.0
            lnLenght=0.0
            ratioLenght=0.0
            
            lpArea=0.0
            lnArea=0.0
            ratioArea=0.0

            lpHausdorff=0.0
            lnHausdorff=0.0
            lpHausdorffMin=0.0
            lpHausdorffMax=0.0
            lnHausdorffMin=0.0
            lnHausdorffMax=0.0
            Hausdorff=0.0

            for mode in contours[slc][frm]: #modif to the cycle not start for 'rn'
                # choose color
                cntrs = []
                if mode == 'lp' or mode == 'ln':
                    cntrs.append(contours[slc][frm][mode])

                #Calculations lp mode
                if mode == 'lp':
                    if cntrs:
                        for i in range(cntrs[0].shape[0]):
                            #Calculate contour lenght
                            lpLenght=lpLenght+math.sqrt(((cntrs[0][i][0]-cntrs[0][i-1][0])**2)+((cntrs[0][i][1]-cntrs[0][i-1][1])**2))
                            #Calculate area
                            lpArea=lpArea+(((cntrs[0][i-1][0]*cntrs[0][i][1])-(cntrs[0][i][0]*cntrs[0][i-1][1]))/2)
                            #Calculate Hausdorff distance
                            if 'ln' in contours[slc][frm]:
                                lpPointX=cntrs[0][i][0]
                                lpPointY=cntrs[0][i][1]
                                for j in range(contours[slc][frm]['ln'].shape[0]): 
                                    lpHausdorff=math.sqrt(((lpPointX-contours[slc][frm]['ln'][j][0])**2)+((lpPointY-contours[slc][frm]['ln'][j][1])**2))
                                    if lpHausdorffMin==0:
                                        lpHausdorffMin=lpHausdorff
                                    if lpHausdorff < lpHausdorffMin:
                                        lpHausdorffMin=lpHausdorff
                                if lpHausdorffMin > lpHausdorffMax:
                                    lpHausdorffMax=lpHausdorffMin
                            lpHausdorff=0.0

                #Calculations ln mode
                if mode == 'ln':
                    if cntrs:
                        for i in range(cntrs[0].shape[0]):
                            lnLenght=lnLenght+math.sqrt(((cntrs[0][i][0]-cntrs[0][i-1][0])**2)+((cntrs[0][i][1]-cntrs[0][i-1][1])**2))
                            #Calculate area
                            lnArea=lnArea+(((cntrs[0][i-1][0]*cntrs[0][i][1])-(cntrs[0][i][0]*cntrs[0][i-1][1]))/2)
                            #Calculate Hausdorff distance
                            if 'lp' in contours[slc][frm]:
                                lnPointX=cntrs[0][i][0]
                                lnPointY=cntrs[0][i][1]
                                for j in range(contours[slc][frm]['lp'].shape[0]):
                                    lnHausdorff=math.sqrt(((lnPointX-contours[slc][frm]['lp'][j][0])**2)+((lnPointY-contours[slc][frm]['lp'][j][1])**2))
                                    if lnHausdorffMin==0:
                                        lnHausdorffMin=lnHausdorff
                                    if lnHausdorff < lnHausdorffMin:
                                        lnHausdorffMin=lnHausdorff
                                if lnHausdorffMin > lnHausdorffMax:
                                    lnHausdorffMax=lnHausdorffMin
                            lnHausdorff=0.0

                Hausdorff=max(lnHausdorffMax, lpHausdorffMax)
                        
                if lpLenght!=0 and lnLenght!=0: #fill up dictionary
                    if slc not in patientdict:
                        if (abs(frm-9) > abs(frm-24)) or frm==0:
                            patientdict[slc] = {}
                            if frm not in patientdict[slc]:
                                patientdict[slc][frm] = {}
                            if 'lpLenght' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lpLenght']=lpLenght
                            if 'lnLenght' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lnLenght']=lnLenght
                            ratioLenght = lpLenght / lnLenght
                            patientdict[slc][frm]['ratioLenght']=ratioLenght
                            if 'lpArea' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lpArea']=lpArea
                            if 'lnArea' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lnArea']=lnArea
                            ratioArea = lpArea / lnArea
                            patientdict[slc][frm]['ratioArea']=ratioArea
                            if 'HausdorffDistance' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['HausdorffDistance']=Hausdorff
                ratioLenght=0.0
                ratioArea=0.0
                #mindent nullázni

            # if len(cntrs) > 0:
            #    draw(image, cntrs, [1, 1, 1])
    print('patient data created for patient with ID:' + validID[x])

print('finished')