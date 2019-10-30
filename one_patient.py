# Reads the sa folder wiht dicom files and contours
# then draws the contours on the images.

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
        #print ("slice: "+str(slc)+" frame: "+str(frm))
        patientdict.update ({"slice":slc})
        patientdict.update ({"frame":frm})
        greensize=0
        redsize=0
        if slc not in patientdict:
            patientdict[slc] = {}
        if frm not in patientdict[slc]:
            patientdict[slc][frm] = {}

        patientdict[slc][frm]['green'] = 213
        patientdict[slc][frm]['red'] = 213

        
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
            # calculate contour size
            print(cntrs[0])
            if mode == 'lp':
                if cntrs:
                    for i in range(len(cntrs[0])):
                        greensize=greensize+1
                    #print ("greensize: "+str(greensize))
                    patientdict.update ({"greensize":greensize})
            
            if mode == 'ln':
                if cntrs:
                    for i in range(len(cntrs[0])):
                        redsize=redsize+1
                    #print ("redsize: "+str(redsize))
                    patientdict.update({"redsize":redsize})
        #print (greensize, redsize)
        if greensize!=0 and redsize!=0:
            ratio = greensize / redsize
            patientdict.update({"ratio":ratio})
        #print(patientdict)
        patientdict.clear()

        #if len(cntrs) > 0:
        #    draw(image, cntrs, rgbs)