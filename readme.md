已经对原来项目chineseocr进行了删减没用的数据.
模型数据都存在了这里,方便下载.也可以去setup.md里面找百度云链接.
https://v2.fangcloud.com/share/f9fe056b9d78b3b98a548ec68d


pytorch:1.1.0版本!!!!!!!!!


manage.py
用flask来开启服务,就这一个文件够了.


运行python manage.py
请求:
116.196.87.166:5080

pic:  img.jpeg










下一步看这种深度网络模型如何服务模型文件,锁内存中,来提高访问速度?
目前只想到了静态变量来提高速度.
然后看看如何加入文字识别方向,现在是4个方向,感觉至少弄成8个方向才够.

2019-09-12,22点17
好像可以用with 语句来保存模型的内部东西
https://www.jianshu.com/p/43da2553a2fb

https://www.imooc.com/wenda/detail/468056





2019-09-13,11点00
部署细节:
直接把import这种东西都放test.py的函数外面,就始终放内存中了.提高检测速度了.!


2019-09-13,15点47
目前有几个问题:
字体大小不一时候识别不准
竖着写字,比如春联时候完全识别不了.  #打算先从这个入手,只需要做一套竖着识别的,然后看2个比分,竖着搞就返回竖着的结果
#横着搞就返回恒这个的结果.




手写识别也垃圾.

解决nms显卡调用问题:
pushd text/detector/utils && sh make.sh && popd
运行完就可以使用c语言nms了.




2019-09-13,23点49
总结:
写numpy时候一定要指定float32类型.防止bug


debug时候利用evaluate:
Image.fromarray(img).save('99999999.png') 随时看图片的过程!!!!!!! 相当霸道的方法.

2019-09-14,1点19

解决不了竖直文字的书写识别

感觉应该换思路,加强识别性即可.


因为1.竖写文字的图片少.如果单字识别高.一样能识别出来.以后相关笔记就写readme里面了


说明结果:

{
    "picName": "700_0",
    "parser": [
        {
            "cx": 593.5,
            "cy": 343.5,
            "text": "益海岳烟注齐母部兴办开于齐",
            "w": 843.3499999999999,
            "h": 61.0,
            "degree": 0.0
        }
    ],
    "angle": 270   #表示逆时针的旋转.
}

所以再做一个不旋转的结果.两个进行比较.
调试还是需要丘比特,反复读参数模型太慢了.





2019-09-14,23点33
解决了旋转问题.


我
是
谁




2019-09-15,16点41

已经知道为什么有的字没法识别了.
关键就是




_, result2, angle2, scores2,tex_rec,newBox2,boxForSingle2,scoresForSingle2,keepIndexForSingle2\
    ,tp_groups2,Allboxes= model.model(cv2.imread(p)   ,
                                       detectAngle=False,  ##是否进行文字方向检测
                                       config=dict(MAX_HORIZONTAL_GAP=50,  ##字符之间的最大间隔，用于文本行的合并
                                                   MIN_V_OVERLAPS=0.6,
                                                   MIN_SIZE_SIM=0.6,
                                                   TEXT_PROPOSALS_MIN_SCORE=0.05,
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
                                       
                                       
这个函数里面的参数.
下面对里面的参数全部做一个说明
1.         detectAngle 当图片旋转了90,180,270的时候可以试着开着.虽然开,但是结果依然不准.模型估计有问题.
所以尽量做2词判断,根据最后得分来选择最好的结果.
2.         MAX_HORIZONTAL_GAP 这个表示次与此之间最大的间隔,字写的越大,这个就开越大
3.                   MIN_V_OVERLAPS 这个参数表示只有竖直香蕉比大于这个数才会看做一行.如果书写的上下越不整齐就把这个参数
改的越小

4.TEXT_PROPOSALS_MIN_SCORE  这个参数最重要.表示汉子识别敏感度,只有大于这个数值的才叫汉子.默认0.1
但是发现很多字识别不出来.可以根据业务多测试看看


5.TEXT_PROPOSALS_NMS_THRESH  :nms算法里面的参数.越大表示nms越宽松.这里面0.3表示2个框香蕉0.3就扔掉得分小的.
6.TEXT_LINE_NMS_THRESH 文本行之间的nms 跟上面一样. 越低表示越严格!!!!!!!!!!!


7.alph ,汉子行的拓展系数.感觉越高越好.


8.注意nms算法,使用python_num版本.gpu版本有bug会算错.应该是c的代码有问题.


2019-09-15,20点12

改进了行组合算法.
因为汉子的边缘应该降低score mask的标准.目前使用的倍率是1.3倍.即
中央文字的score阈值是边缘阈值的1.3倍

所以现在的TEXT_PROPOSALS_MIN_SCORE 表示边缘的识别汉子阈值.

2019-09-15,20点13

下面还继续改进.


预处理函数.








