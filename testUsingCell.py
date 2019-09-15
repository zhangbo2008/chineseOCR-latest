#把引入模块都放入静态区域!!!!!!!!!!!!!
#他们在的区域是堆中,因为服务一直没停,所以一直占用内存.正好是我们需要的效果!!!!!!!!!!!!!!!!!!!!
#发现会重复引入下面的库包,加一个引用计数.也不行,用locals加flag也不行!!!

"""这个文件是用于测试"""
## 如果修改了原来的模块,那么就del 然后再import?????好像还是不行.
#只能点击pycharm 里面的+号按钮,重新建立一个python console
##
if 'flag'  not in   locals():
    flag=1

    import os

    GPUID = '0'  ##调用GPU序号
    os.environ["CUDA_VISIBLE_DEVICES"] = GPUID
    import torch
    from apphelper.image import xy_rotate_box, box_rotate, solve
    import model

    #注意目前只支持4个方向,我要做成8个方向的,只是图片预处理时候多算几个方向即可.4个感觉不够.
    import cv2
    import numpy as np
    print("zhuangzaile moxing")




    def plot_boxes1(img,boxes):
        blue = (0, 0, 0) #18
        tmp = np.copy(img)
        for box in boxes:
             cv2.rectangle(tmp, (int(box[0]),int(box[1])), (int(box[2]), int(box[3])), blue, 1) #19
        out=Image.fromarray(tmp).convert('RGB')
        out.save("保存的图片看box.jpg")
        return Image.fromarray(tmp)

    def plot_boxes2(img,angle, result,color=(0,0,0)):
        tmp = np.array(img)
        c = color
        h,w = img.shape[:2]
        thick = int((h + w) / 300)
        i = 0
        if angle in [90,270]:
            imgW,imgH = img.shape[:2]

        else:
            imgH,imgW= img.shape[:2]

        for line in result:
            cx =line['cx']
            cy = line['cy']
            degree =line['degree']
            w  = line['w']
            h = line['h']

            x1,y1,x2,y2,x3,y3,x4,y4 = xy_rotate_box(cx, cy, w, h, degree/180*np.pi)

            x1,y1,x2,y2,x3,y3,x4,y4 = box_rotate([x1,y1,x2,y2,x3,y3,x4,y4],angle=(360-angle)%360,imgH=imgH,imgW=imgW)
            cx  =np.mean([x1,x2,x3,x4])
            cy  = np.mean([y1,y2,y3,y4])
            cv2.line(tmp,(int(x1),int(y1)),(int(x2),int(y2)),c,1)
            cv2.line(tmp,(int(x2),int(y2)),(int(x3),int(y3)),c,1)
            cv2.line(tmp,(int(x3),int(y3)),(int(x4),int(y4)),c,1)
            cv2.line(tmp,(int(x4),int(y4)),(int(x1),int(y1)),c,1)
            mess=str(i)
            cv2.putText(tmp, mess, (int(cx), int(cy)),0, 1e-3 * h, c, thick // 2)
            i+=1
        out=Image.fromarray(tmp).convert('RGB')
        out.save("保存的图片.jpg")
        return out




#下面是函数主体.

##
#发现目前还是文字框,沙没法识别出来,当2行比较近时候就不行!!!!!!!!!!!!!!!!!!!!!!
'''


        沙
        我



'''

#2019-09-15,11点39开始继续搞识别.
#讨论的,沙竖着写识别不出来.为什么? 发现沙字下面写什么字,多会导致沙没法识别.

#发现观察图片时候需要一个按照像素移动鼠标的功能.  这个好像是nms算法的缺陷.
#https://www.cnblogs.com/zf-blog/p/8532228.html
import time
from PIL import Image
import os,sys
p = 'tmp4.png'
img = cv2.imread(p)






def depoint(img):   #input: gray image  #去燥方案.
    pixdata = img
    pixdata =  cv2.cvtColor(pixdata, cv2.COLOR_BGR2GRAY)  # 保证不改变代码其他位置
    print(pixdata.shape)
    w,h = pixdata.shape
    for y in range(1,h-1):
        for x in range(1,w-1): #锐化,去除边缘的像素,边缘的像素周围会有接近于0的点.
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    pixdata = src_RGB = cv2.cvtColor(pixdata, cv2.COLOR_GRAY2BGR)  # 保证不改变代码其他位置
    pixdata = cv2.fastNlMeansDenoisingColored(pixdata, None, 10, 10, 7, 21)
    cv2.imwrite('11111.png',pixdata)
    print(pixdata.shape)
    return pixdata
img=depoint(img)
Image.fromarray(img).save("23321321.png")#看看预处理之后的结果.
TEXT_LINE_NMS_THRESH=0.8
h,w = img.shape[:2]
timeTake = time.time()
print(111111111111)
#这个scores1,socres2. 直接sum效果不好.因为很多差的边框会扰乱结果.所以需要先nms再算score
_,result1,angle1,scores1,tex_rec,newBox,boxForSingle,scoresForSingle,keepIndexForSingle\
    ,tp_groups= model.model(img,
                                    detectAngle=True,##是否进行文字方向检测
                                    config=dict(MAX_HORIZONTAL_GAP=50,##字符之间的最大间隔，用于文本行的合并
                                    MIN_V_OVERLAPS=0.6,
                                    MIN_SIZE_SIM=0.6,
                                    TEXT_PROPOSALS_MIN_SCORE=0.1,
                                    TEXT_PROPOSALS_NMS_THRESH=0.3,
                                    TEXT_LINE_NMS_THRESH = TEXT_LINE_NMS_THRESH,##文本行之间测iou值

                ),
                                    leftAdjust=True,##对检测的文本行进行向左延伸
                                    rightAdjust=True,##对检测的文本行进行向右延伸
                                    alph=0.03,##对检测的文本行进行向右、左延伸的倍数

                                   )
print(result1)

_, result2, angle2, scores2,tex_rec,newBox2,boxForSingle2,scoresForSingle2,keepIndexForSingle2\
    ,tp_groups2= model.model(cv2.imread(p)   ,
                                       detectAngle=False,  ##是否进行文字方向检测
                                       config=dict(MAX_HORIZONTAL_GAP=50,  ##字符之间的最大间隔，用于文本行的合并
                                                   MIN_V_OVERLAPS=0.6,
                                                   MIN_SIZE_SIM=0.6,
                                                   TEXT_PROPOSALS_MIN_SCORE=0.1,
                                                   TEXT_PROPOSALS_NMS_THRESH=0.3,
                                                   TEXT_LINE_NMS_THRESH=TEXT_LINE_NMS_THRESH,  ##文本行之间测iou值
                                                   #需要修改上面这个参数,来让行识别率提升.
                                                   #参数越大,iou大于阈值的才会扔掉.
                                                   #所以越大结果越多.

                                                   ),
                                       leftAdjust=True,  ##对检测的文本行进行向左延伸
                                       rightAdjust=True,  ##对检测的文本行进行向右延伸
                                       alph=0.03,  ##对检测的文本行进行向右、左延伸的倍数

                                       )

print(result2)




#画出结果:
try:
    plot_boxes1(img, boxForSingle[tp_groups[0]])
except:
    plot_boxes1(img, boxForSingle2[tp_groups2[0]])








##
if scores1.sum()>scores2.sum():

    out={}

    out['picName']='tmp'
    out['parser']=result1
    out['angle']=angle1

##
out={}

out['picName']='tmp'
out['parser']=result2
out['angle2']=angle2



    # In[ ]:

'''


的




沙


发
斯

蒂
芬



'''
#对于图片结果,用画图打开之后,移动鼠标会看到对应的坐标.

## 测试cv的横纵.
im=cv2.imread('tmp.png')


im=im[0:250,100:250] # 是h,w 第二列是横坐标,第一列是纵坐标.
cv2.imwrite('11111.png',im)





##

#下面测试图像预处理方法:


def depoint():   #input: gray image  #去燥方案.
    pixdata = cv2.imread('tmp.png',flags=0)
    print(pixdata.shape)
    w,h = pixdata.shape
    for y in range(1,h-1):
        for x in range(1,w-1): #锐化,去除边缘的像素,边缘的像素周围会有接近于0的点.
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    pixdata=src_RGB = cv2.cvtColor(pixdata, cv2.COLOR_GRAY2BGR)#保证不改变代码其他位置
    pixdata = cv2.fastNlMeansDenoisingColored(pixdata, None, 10, 10, 7, 21)
    cv2.imwrite('11111.png',pixdata)
    print(pixdata.shape)
    return pixdata

depoint()


#https://www.jianshu.com/p/921c1da740b5


##
