import image
import math
pi=math.pi
x=0
y=0
cx=1
cy=1
angle = 90*pi/180
newx,newy=image.rotate(x,y,angle,cx,cy)
print(newx,newy)
import numpy as np
img=np.zeros([1,3,4])
print(img)
tmpOld=np.zeros_like(img)
print(tmpOld)
tmpOld.fill(255)
print(tmpOld)

def rotate_boxNishi90(box):
    h=box[3]-box[1]
    w=box[2]-box[0]
    center=(box[0]+box[2])/2,(box[1]+box[3])/2
    zuoshang=center[0]-h/2,center[1]-w/2
    youxia=center[0]+h/2,center[1]+w/2
    return zuoshang,youxia


print(rotate_boxNishi90([0,0,1,2]))
