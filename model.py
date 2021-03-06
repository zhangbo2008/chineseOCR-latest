# -*- coding: utf-8 -*-
from config import opencvFlag,GPU,IMGSIZE,ocrFlag
if not GPU:
    import os
    os.environ["CUDA_VISIBLE_DEVICES"]=''##不启用GPU

if ocrFlag=='torch':
    from crnn.crnn_torch import crnnOcr as crnnOcr ##torch版本ocr
elif ocrFlag=='keras':
     from crnn.crnn_keras import crnnOcr as crnnOcr ##keras版本OCR

import time
import cv2
import numpy as np
from PIL import Image
from glob import glob

from text.detector.detectors import TextDetector
from apphelper.image import get_boxes,letterbox_image

from text.opencv_dnn_detect import angle_detect##文字方向检测,支持dnn/tensorflow
from apphelper.image import estimate_skew_angle ,rotate_cut_img,xy_rotate_box,sort_box,box_rotate,solve

if opencvFlag=='opencv':
    from text import opencv_dnn_detect as detect ##opencv dnn model for darknet
elif opencvFlag=='darknet':
    from text import darknet_detect as detect
else:
    # keras版本文字检测
    from text import keras_detect as detect

print("Text detect engine:{}".format(opencvFlag))



def text_detect(img,
                MAX_HORIZONTAL_GAP=30,
                MIN_V_OVERLAPS=0.6,
                MIN_SIZE_SIM=0.6,
                TEXT_PROPOSALS_MIN_SCORE=0.7,
                TEXT_PROPOSALS_NMS_THRESH=0.3,
                TEXT_LINE_NMS_THRESH = 0.3,bili=1.2
                ):#下面8行检测单个文字

    #下面几行是用yolo给出框.
    Image.fromarray(img).save("look.png")#看看boxes,scores的含义 是所有rpn的结果.
    boxes, scores = detect.text_detect(np.array(img))  #这里面用的是yolo
    boxes = np.array(boxes,dtype=np.float32)
    scores = np.array(scores,dtype=np.float32)

    Allboxes=boxes
    AllScores=scores


#函数下面部分是做行拼接.
    textdetector  = TextDetector(MAX_HORIZONTAL_GAP,MIN_V_OVERLAPS,MIN_SIZE_SIM)

    shape = img.shape[:2]

    #看看下行boxes 的含义.  scores:表示最后抽取的汉字对应的score?????????对的,下行的scores就是最后每行的
    #分数了!!!!!!!!!!!!!1 非常重要的参数. #下面几行做文字box拼接成seq #tp_groups 表示每一行的文字对应
    #boxesForSingle 中的index
    boxes,scores,keepIndForSingle,tp_groups,boxesForSingle,scoresForSingle= textdetector.detect(boxes,
                                scores[:, np.newaxis],
                                shape,
                                TEXT_PROPOSALS_MIN_SCORE,
                                TEXT_PROPOSALS_NMS_THRESH,
                                TEXT_LINE_NMS_THRESH,bili
                                )
    #tp_groups 是boxes对应的 box标号.
    text_recs = get_boxes(boxes)

    print(text_recs.shape,"text_recs.shape")
    newBox = []
    rx = 1
    ry = 1
    for box in text_recs:
           x1,y1 = (box[0],box[1])
           x2,y2 = (box[2],box[3])
           x3,y3 = (box[6],box[7])
           x4,y4 = (box[4],box[5])
           newBox.append([x1*rx,y1*ry,x2*rx,y2*ry,x3*rx,y3*ry,x4*rx,y4*ry])

    return newBox ,scores,boxesForSingle,scoresForSingle,keepIndForSingle,tp_groups,Allboxes,AllScores



def crnnRec(im,boxes,leftAdjust=False,rightAdjust=False,alph=0.2,f=1.0,tp_groups=None,boxAll=None,scoreAll=None):
   """
   crnn模型，ocr识别
   leftAdjust,rightAdjust 是否左右调整box 边界误差，解决文字漏检
   """
   results = []
   im = Image.fromarray(im) 
   for index,box in enumerate(boxes):
       degree,w,h,cx,cy = solve(box)
       partImg,newW,newH = rotate_cut_img(im,degree,box,w,h,leftAdjust,rightAdjust,alph)
       text = crnnOcr(partImg.convert('L'))

       detailbox=boxAll[tp_groups[index]]
       detailscore=scoreAll[tp_groups[index]]
       detaildex=tp_groups[index]


       if text.strip()!=u'':
            results.append({'cx':cx*f,'cy':cy*f,'text':text,'w':newW*f,'h':newH*f,'degree':degree*180.0/np.pi
,'detailbox':detailbox,'detailscore':detailscore,'detaildex':detaildex

                            })
 #degree表示顺时针转多少度.
   return results




def eval_angle(im,detectAngle=False):
    """
    估计图片偏移角度
    @@param:im
    @@param:detectAngle 是否检测文字朝向
    """
    angle = 0
    img = np.array(im)
    if detectAngle:
        angle = angle_detect(img=np.copy(img))##文字朝向检测
        if angle==90:
            im = Image.fromarray(im).transpose(Image.ROTATE_90)
        elif angle==180:
            im = Image.fromarray(im).transpose(Image.ROTATE_180)
        elif angle==270:
            im = Image.fromarray(im).transpose(Image.ROTATE_270)
        img = np.array(im)
        
    return  angle,img


def model(img,detectAngle=False,config={},leftAdjust=False,rightAdjust=False,alph=0.2,bili=1.2):
    """
    @@param:img,
    @@param:ifadjustDegree 调整文字识别倾斜角度
    @@param:detectAngle,是否检测文字朝向
    """
    print(22222222222)
    '''
    这个地方需要加入图片预处理!!!!!!滤波等.
    
    确实这个算法没有加入,需要加入!!!!!!!!!!!
    '''









    angle,img = eval_angle(img,detectAngle=detectAngle)##文字方向检测



    if opencvFlag!='keras':
       img,f =letterbox_image(Image.fromarray(img), IMGSIZE)## pad
       img = np.array(img)
    else:
        f=1.0##解决box在原图坐标不一致问题
    
    config['img'] = img
    config['bili'] = bili
    text_recs, scores, boxForSingleAfterNMS, scoresForSingle, keepIndForSingle, tp_groups,Allboxes,Allscores = text_detect(**config)##文字检测
    newBox,tp_groups = sort_box(text_recs,tp_groups)  #按照列高排序,符合我们阅读顺序!     ##下行行文本识别
    print(newBox)
    result = crnnRec(np.array(img),newBox,leftAdjust,rightAdjust,alph,1.0/f,tp_groups,boxForSingleAfterNMS,scoresForSingle)
    return img, result, angle, scores, text_recs, newBox, boxForSingleAfterNMS, scoresForSingle, keepIndForSingle, tp_groups,Allboxes,Allscores




#keepIndForSingle 表示到底哪个index 对于boxForSingle 中的东西,最后再图片中得到了使用.
#tp_groups, 每一行行文字取的dex



