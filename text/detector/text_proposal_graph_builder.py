import numpy as np
class Graph:
    def __init__(self, graph):
        self.graph=graph

    def sub_graphs_connected(self):
        sub_graphs=[]  #利用临街矩阵拼接.
        for index in range(self.graph.shape[0]):
            if not self.graph[:, index].any() and self.graph[index, :].any():#如果index的前节点没有,后节点有就进入
                v=index
                sub_graphs.append([v])
                while self.graph[v, :].any():
                    v=np.where(self.graph[v, :])[0][0]   #得到后续节点的index
                    sub_graphs[-1].append(v)
        return sub_graphs#得到最后的一组值!!!!!表示seq


class TextProposalGraphBuilder:
    """
        Build Text proposals into a graph.
    """
    def __init__(self,MAX_HORIZONTAL_GAP=30,MIN_V_OVERLAPS=0.6,MIN_SIZE_SIM=0.6):
        """
        @@param:MAX_HORIZONTAL_GAP:文本行间隔最大值
        @@param:MIN_V_OVERLAPS
        @@param:MIN_SIZE_SIM
        MIN_V_OVERLAPS=0.6
        MIN_SIZE_SIM=0.6
        """
        self.MAX_HORIZONTAL_GAP = MAX_HORIZONTAL_GAP
        self.MIN_V_OVERLAPS = MIN_V_OVERLAPS
        self.MIN_SIZE_SIM = MIN_SIZE_SIM
    #获取index这个box的后续同行坐标.
    def get_successions(self, index):
            box=self.text_proposals[index]
            results=[]
            for left in range(int(box[0])+1, min(int(box[0])+self.MAX_HORIZONTAL_GAP+1, self.im_size[1])):
                adj_box_indices=self.boxes_table[left] #阻个像素开始找,从开始x坐标到maxgap+x开始坐标.
                for adj_box_index in adj_box_indices: #表示和box变量相连的坐标
                    if self.meet_v_iou(adj_box_index, index):#如果临街box存在.
                        results.append(adj_box_index)
                if len(results)!=0:
                    return results
            return results

    def get_precursors(self, index):
        box=self.text_proposals[index]#查询2这个节点的前面节点是几?
        results=[]
        for left in range(int(box[0])-1, max(int(box[0]-self.MAX_HORIZONTAL_GAP), 0)-1, -1):
            adj_box_indices=self.boxes_table[left]
            for adj_box_index in adj_box_indices:
                if self.meet_v_iou(adj_box_index, index):
                    results.append(adj_box_index)
            if len(results)!=0:
                return results
        return results

    def is_succession_node(self, index, succession_index):
        precursors=self.get_precursors(succession_index)
        #如果积分比前面的差就不要了.#确实需要这么判断,比如2个字符a,b  b是a的最优后续节点,但是a不是b的最优 #前置节点,而c是b的最优前置节点.那么就不能让ab拼接成一个单词.
        if self.scores[index]>=np.max(self.scores[precursors]):
            return True
        return False

    def meet_v_iou(self, index1, index2): #返回汉子之间的iou是否符合相邻汉子的标准.
        def overlaps_v(index1, index2):
            h1=self.heights[index1]
            h2=self.heights[index2]
            y0=max(self.text_proposals[index2][1], self.text_proposals[index1][1])
            y1=min(self.text_proposals[index2][3], self.text_proposals[index1][3])
            return max(0, y1-y0+1)/min(h1, h2) #表示2个汉子的竖直方向的重合比例.越高表示越在同一个水平线上!

        def size_similarity(index1, index2):
            h1=self.heights[index1]
            h2=self.heights[index2]
            return min(h1, h2)/max(h1, h2)  #表示2个汉子的竖直方向高度的相似比例.

        return overlaps_v(index1, index2)>=self.MIN_V_OVERLAPS and \
               size_similarity(index1, index2)>=self.MIN_SIZE_SIM

    def build_graph(self, text_proposals, scores, im_size):
        self.text_proposals=text_proposals
        self.scores=scores
        self.im_size=im_size
        self.heights=text_proposals[:, 3]-text_proposals[:, 1]+1 #每一个box的高度
        boxes_table=[[] for _ in range(self.im_size[1])] #im_size=(h,w) boxes_table[i] 表示像素第i行相交的矩阵index表
        for index, box in enumerate(text_proposals):
            #print(int(box[0]),len(boxes_table))
            boxes_table[int(box[0])].append(index) #把数据扔到boxes_table里面.用第0个坐标(也就是左下角)来表示这个box
        self.boxes_table=boxes_table

        graph=np.zeros((text_proposals.shape[0], text_proposals.shape[0]), np.bool)#所有的box之间建立邻接矩阵
        '''
        graph 经过下面的处理变成一个链表. 一个是index一个是succession_index 表示下一个
        相连接的box的index    用一个相关矩阵来表示.
        '''
        for index, box in enumerate(text_proposals):
            #下面一行是关键.
            successions=self.get_successions(index) #比如这里0的后续是2
            if len(successions)==0:
                continue
            succession_index=successions[np.argmax(scores[successions])]#如果有多个后续的时候,用argmax提取出一个最好的!
            if self.is_succession_node(index, succession_index):#再一次进行判断.
                # NOTE: a box can have multiple successions(precursors) if multiple successions(precursors)
                # have equal scores.
                graph[index, succession_index]=True #如果成立邻接矩阵就置1.
        return Graph(graph)
