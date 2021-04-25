import cv2
import os
import numpy as np

def crop_image(img,tol=0):
    # img is 2D image data
    # tol  is tolerance
    mask = img>tol
    return img[np.ix_(mask.any(1),mask.any(0))]


fileDir = os.path.dirname(os.path.abspath(__file__))

link_jpg = fileDir + "/images/image_original.JPG"
path = fileDir + "/images/rendered"
outputfolder = fileDir + "/images/matched"
result = fileDir + "/images/result"

bestscore = 0

for link in os.listdir(path):
    img = cv2.imread(link_jpg,0)
    img2 = img.copy()
    template = cv2.imread(os.path.join(path,link),0)
    template = crop_image(template, 100)
    if not os.path.exists(os.path.join(outputfolder, "cropped")):
        os.makedirs(os.path.join(outputfolder, "cropped"))
    cv2.imwrite(os.path.join(outputfolder, "cropped",link), template)
    w, h = template.shape[::-1]

    img = img2.copy()
    method = eval('cv2.TM_CCOEFF')

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    crop_img = img[top_left[1]:top_left[1]+h, top_left[0]:top_left[0]+w]
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    cv2.imwrite(os.path.join(outputfolder,link), crop_img)

    if(bestscore < max_val):
        bestmatch = crop_img
        bestlink = link
    print(max_val)
    print(link)


if not os.path.exists(result):
    os.makedirs(result)
cv2.imwrite(os.path.join(result,bestlink), bestmatch)
