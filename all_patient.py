# Reads the sa folder wiht dicom files and contours
# then draws the contours on the images.
import math
import os
import pickle
#import Make_pickle
from con_reader import CONreaderVM
from dicom_reader import DCMreaderVM
from con2img import draw_contourmtcs2image as draw
import numpy as np
from numpy.linalg import eig, inv

def fitEllipse(x,y):
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    axis1=np.sqrt(up/down1)
    axis2=np.sqrt(up/down2)
    return axis1, axis2

picklePath = r'C:\Repoz\LHYP'
PickleList = []
files = os.listdir(picklePath)
for FileName in files:
    if FileName.endswith(".pickle"):
        PickleList.append(FileName)

patientdict=dict()

for x in range(len(PickleList)):
    pickle_in = open(PickleList[x],"rb")
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
                            #calculate ellipse
                            X = cntrs[0][:, 0]
                            Y = cntrs[0][:, 1]
                            ellipseResult = fitEllipse(X, Y)
                            lpMajorAxis = ellipseResult[0]
                            lpMinorAxis = ellipseResult[1]

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
                            #calculate ellipse
                            X = cntrs[0][:, 0]
                            Y = cntrs[0][:, 1]
                            ellipseResult = fitEllipse(X, Y)
                            lnMajorAxis = ellipseResult[0]
                            lnMinorAxis = ellipseResult[1]
                            
                Hausdorff=max(lnHausdorffMax, lpHausdorffMax)
                        
                if lpLenght!=0 and lnLenght!=0: #fill up dictionary
                    if slc not in patientdict:
                        if (abs(frm-9) > abs(frm-24)) or frm==0:
                            ratioLenght = lpLenght / lnLenght
                            ratioArea = lpArea / lnArea
                            majorAxisRatio = lpMajorAxis / lnMajorAxis
                            minorAxisRatio = lpMinorAxis / lnMinorAxis

                            patientdict[slc] = {}
                            if frm not in patientdict[slc]:
                                patientdict[slc][frm] = {}
                            if 'lpLenght' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lpLenght']=lpLenght
                            if 'lnLenght' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lnLenght']=lnLenght
                            if 'ratioLenght' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['ratioLenght']=ratioLenght

                            if 'lpArea' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lpArea']=lpArea
                            if 'lnArea' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['lnArea']=lnArea
                            if 'ratioArea' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['ratioArea']=ratioArea

                            if 'HausdorffDistance' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['HausdorffDistance']=Hausdorff

                            if 'MinorAxisRatio' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['MinorAxisRatio']=minorAxisRatio
                            if 'MajorAxisRatio' not in patientdict[slc][frm]:
                                patientdict[slc][frm]['MajorAxisRatio']=majorAxisRatio

                #mindent nullázni
                ratioLenght=0.0
                ratioArea=0.0
                majorAxisRatio=0.0
                minorAxisRatio=0.0

    

print('finished')