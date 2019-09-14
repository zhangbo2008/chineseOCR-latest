import cv2
image=cv2.imread('tmp.jpg',0)

rows,cols = image.shape
print(rows,cols) #所以中心点事
#https://segmentfault.com/a/1190000015645951?utm_source=tag-newest
M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
dat=cv2.warpAffine(image,M,(cols,rows))

'''
还是pil好用,cv太难用
'''
from PIL import Image

from PIL import Image
import matplotlib.pyplot as plt


dat=Image.fromarray(image).transpose(Image.ROTATE_90)






dat.save('dst111111111111111111111111.png')  #还是pil完美!





'''
截取:
'''










