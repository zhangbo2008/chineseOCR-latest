import numpy as np
from text.detector.text_proposal_graph_builder import TextProposalGraphBuilder

class TextProposalConnector:
    """
        Connect text proposals into text lines
    """
    def __init__(self,MAX_HORIZONTAL_GAP=30,MIN_V_OVERLAPS=0.6,MIN_SIZE_SIM=0.6):
        self.graph_builder=TextProposalGraphBuilder(MAX_HORIZONTAL_GAP,MIN_V_OVERLAPS,MIN_SIZE_SIM)

    def group_text_proposals(self, text_proposals, scores, im_size):
        graph=self.graph_builder.build_graph(text_proposals, scores, im_size)
        return graph.sub_graphs_connected()

    def fit_y(self, X, Y, x1, x2):
        len(X)!=0
        # if X only include one point, the function will get line y=Y[0]
        if np.sum(X==X[0])==len(X):
            return Y[0], Y[0]
        p=np.poly1d(np.polyfit(X, Y, 1))
        return p(x1), p(x2)

    def get_text_lines(self, text_proposals, scores, im_size,scoresBeforeNor,yuzhi,bili):#画出新的box
        """
        text_proposals:boxes
        
        """
        # tp=text proposal





#text_proposals :676

        #下面一行很核心!!!!!!!!!!!!   im_size: 原始大图片的长和宽
        tp_groups=self.group_text_proposals(text_proposals, scores, im_size)##find the text line 
        #下面对结果拼接box参数设置8






        '''
        自定义的赛选策略
        原理就是汉子边缘的score需求可以放宽
        '''




        notkeep_inds = []
        for i in range(len(tp_groups)):
            if len(tp_groups[i]) > 2:
                tmp = tp_groups[i][1:-1]
                if (scoresBeforeNor[tmp] < yuzhi * bili).any():
                    notkeep_inds.append(i)
        tp_groups = np.delete(np.array(tp_groups), notkeep_inds, axis=0)


        text_lines=np.zeros((len(tp_groups), 8), np.float32)

        #看下面对于tp_groups的处理.

        for index, tp_indices in enumerate(tp_groups):
            text_line_boxes=text_proposals[list(tp_indices)]
            #num = np.size(text_line_boxes)##find 
            X = (text_line_boxes[:,0] + text_line_boxes[:,2]) / 2 #每一个汉子的行中心点
            Y = (text_line_boxes[:,1] + text_line_boxes[:,3]) / 2 #每一个汉子的列中心点
            
            z1 = np.polyfit(X,Y,1)        #拟合成一个新的直线.
           # p1 = np.poly1d(z1)

#从下行看出来,结果实际上是,上面给的框的min和max做括起来的区域.
            x0=np.min(text_line_boxes[:, 0])
            x1=np.max(text_line_boxes[:, 2])

            offset=(text_line_boxes[0, 2]-text_line_boxes[0, 0])*0.5  #第一个汉子的宽*0.5
            #下面一行拟合的直线是得到的seq 上横线的刻画 ,下面第二行是上横线用末端点的另一个刻画.#他俩差别不大.
            lt_y, rt_y=self.fit_y(text_line_boxes[:, 0], text_line_boxes[:, 1], x0+offset, x1-offset)
            lb_y, rb_y=self.fit_y(text_line_boxes[:, 0], text_line_boxes[:, 3], x0+offset, x1-offset)

            # the score of a text line is the average score of the scores
            # of all text proposals contained in the text line
            score=scores[list(tp_indices)].sum()/float(len(tp_indices))

            text_lines[index, 0]=x0
            text_lines[index, 1]=min(lt_y, rt_y) #为了鲁棒性,取2个直线的最大暴裸
            text_lines[index, 2]=x1
            text_lines[index, 3]=max(lb_y, rb_y)
            text_lines[index, 4]=score        #把分数放在这里了!!!!!!!!!!!!!!!!11
            text_lines[index, 5]=z1[0]#记录直线的斜率和bias
            text_lines[index, 6]=z1[1]
            height = np.mean( (text_line_boxes[:,3]-text_line_boxes[:,1]) )#平均字高
            text_lines[index, 7]= height + 2.5#还是为了鲁棒性.
        #text_lines=clip_boxes(text_lines, im_size)




        return text_lines,tp_groups
