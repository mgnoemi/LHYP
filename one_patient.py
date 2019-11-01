# Reads the sa folder wiht dicom files and contours
# then draws the contours on the images.
import math
from con_reader import CONreaderVM
from dicom_reader import DCMreaderVM
from con2img import draw_contourmtcs2image as draw


image_folder = r'C:\Egyetem\MSC\2.félév\Projektfeladat\10635813AMR806\sa\images'
con_file = r'C:\Egyetem\MSC\2.félév\Projektfeladat\10635813AMR806\sa\contours.con'

# reading the dicom files
dr = DCMreaderVM(image_folder)

# reading the contours
cr = CONreaderVM(con_file)
contours = cr.get_hierarchical_contours()
patientdict=dict()
# drawing the contours for the images
for slc in contours:
    for frm in contours[slc]:
        image = dr.get_image(slc, frm)  # numpy array
        #cntrs = []
        rgbs = []
        
        greenlength=0.0
        redlength=0.0
        ratio=0.0

        if slc not in patientdict:
            if (abs(frm-9) > abs(frm-24)) or frm==0:
                patientdict[slc] = {}
                if frm not in patientdict[slc]:
                    patientdict[slc][frm] = {}
       
        for mode in contours[slc][frm]: #modif to the cycle not start for 'rn'
            # choose color
            cntrs = []
            if mode == 'lp':
                rgb = [0, 1, 0]
            elif mode == 'ln':
                rgb = [1, 0, 0]
            else:
                rgb = None
            if rgb is not None:
                cntrs.append(contours[slc][frm][mode])
                rgbs.append(rgb)
            # calculate contour length
            if mode == 'lp':
                if cntrs:
                    for i in range(len(cntrs[0])):
                        greenlength=greenlength+math.sqrt(((cntrs[0][i][0]-cntrs[0][i-1][0])**2)+((cntrs[0][i][1]-cntrs[0][i-1][1])**2))
            if mode == 'ln':
                if cntrs:
                    for i in range(len(cntrs[0])):
                        redlength=redlength+math.sqrt(((cntrs[0][i][0]-cntrs[0][i-1][0])**2)+((cntrs[0][i][1]-cntrs[0][i-1][1])**2))
            if greenlength!=0 and redlength!=0:
                if 'green' not in patientdict[slc][frm]:
                    patientdict[slc][frm]['green']=greenlength
                if 'red' not in patientdict[slc][frm]:
                    patientdict[slc][frm]['red']=redlength

        if greenlength!=0 and redlength!=0:
            ratio = greenlength / redlength
            patientdict[slc][frm]['ratio']=ratio
        else:
            ratio=0.0

print(patientdict)

        #if len(cntrs) > 0:
        #    draw(image, cntrs, rgbs)