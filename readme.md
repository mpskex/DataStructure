#   数据结构课程设计

#   Class
## ***SinglePath***
Provide node to node shortest path calculation Service

|Attributes  | Note|
|:------|:-----|
|INIFINITE  |   Infinite value should be pre procceed, for example 9999|
|dist_map   |   Origin Map data from file|
|neigh_map  |   Origin Generated from the Origin map from file|
|dist       |   Updated Floyd shortest distance map|
|path       |   Updated Floyd shortest neighbour map|
|map_size   |   size of the map|

|Method |Argument|Note|
|:------|:-----:|:----|
|SGT_Floyd_Update() |   NONE    |   generate the smallest generated tree of this graph|
|SSSP_Floyd()|  node_src, node_dst  |   Single Source Shortest Path|

##  ***MultiPath***
Provide source to destination shortest path calculation Service
Planning route with specified strategy

|Attributes  | Note|
|:------|:-----|
|singlepath |   SinglePath Object|
|keypoints  |   list of keypoints with time cost limit|
|waypoints  |   list of waypoint which is not sensitive to time|
 
|Method |Argument|Note|
|:------|:-----:|:----|
|AddKeyPoint()  |   point, time_cost    |   Add keypoint to list|
|AddWayPoint()  |   point   |   Add waypoint to list|
|CalcMultiPath()    |   point_i |   planning route with specified strategy|

##  ***PathTree***
Structure to exhaust every route possible within the limited cost

|Attributes  | Note|
|:------|:-----|
|NodeTree   |   TreeNode Object which is the root of the PathTree|
 
|Method |Argument|Note|
|:------|:-----:|:----|
|UpdateCost()   |   root, dist_matrix, num=1 |   update the cost of every node|
|CreateTree()   |   parent, child_list, last_leaf   |  create a  path tree|
|ReduceTree()   |   root, dist_matrix, cost_limit, num=1    |   reduce the tree due to the cost limit|
|Print()        |   None    |   Print tree in root first order| 

##  ***TreeNode***
Tree node object that support the link tree structure

|Attributes  | Note|
|:------|:-----|
|child  |   child list cotain TreeNode objects, like chain|
|data   |   here we storage the node number|
|cost   |   cost spent when arrive at this node|
 
|Method |Argument|Note|
|:------|:-----:|:----|
|AddChild()   |   child |   Add a child node to child list|
|SetChilds()   |   child_list   |  Set the child list to a specific node list|
|toString()        |   None    |   Print tree node| 


##  基本要求
*   以图形方式输出各场所平面地图，数据从文件读入，并提供出发时刻。
*   提供所有场所名称，供用户选择，至少包括5个场所，至少包括上课或上机及时间和地点
*   指定出行方式，以动画形式逐一输出线路和到达时刻：首先，在包含所有场所及所有路径的平面图上，标明起点位置，之后，用户每次回车后，能够展示下一条路径和将要到达场所的位置及到达时刻，供用户参考。

##  设计思路
*   使用python作为实现语言。
*   使用flask框架搭建Web应用。
*   Javascript丰富前端界面
*   数据库存取数据，完成扩展功能。
*   松散组织结构，算法主体可以使用本地服务形式提供接入点

##  数据结构设计
*   算法特点
    *   以完全竞赛图作为数学模型，问题可以抽象成在竞赛图中完成最优路径求解的问题
    *   每一次用户添加数据路径点都相当于一次求解过程
    *   可以在用户得到目前最优解后，给出优化后的路线
    *   图以邻接表的形式存储
    *   使用Floyd算法求解单源最短路径
    *   使用python完成所有功能的封装
*   具体数据结构
    *   一个以到达时间要求排序的节点列表
    *   一个没有时间要求的无序目标节点表
    *   一个以最近时间要求节点作为所有叶子结点的路径树
    *   一张地图距离表
    *   三张floyd距离表
    *   三张floyd邻接表
    *   三张不同交通方式时间惩罚系数表
*   具体算法操作
    *   首先更新floyd邻接表，以及距离表（使用系数惩罚表与距离表得出结果）（三张floyd表，三张邻接表）
    *   然后抽取一个关键点（key waypoint），去生成树带权高度不超过限定时间的一个n叉树（其中叶子结点为关键点），选出其中距离最短的一条路径，作为选择的路径，记录并输出
    *   最终输出满足所有关键点的，并访问所有必经节点的路径
*   算法细节
    *   如果已经里边所有关键点，还有必经节点有剩余，那么久遍历所有剩余毕竟节点的组合，并从中计算最短路径。（可以考虑使用图）
    *   如果没有指定关键点，就使用上述算法求出最短解


##  运行环境安排
*   OS:     校内linux (ubuntu 17.04 Server)
*   RE:     flask  (python 2.7)
*   DB:     sqlite3

##  设计理由
*   网页可以作为载体让平台不再是障碍。并且目前又很多能够提供优秀服务的服务框架。可以让定制网页服务得到良好的发挥。
*   python作为一种脚本语言，对热修补有很好支持。算法更新以及网站内容扩展可以在此轻松实现。同时python的可读性很强，代码简洁，方便日后开发与维护。相比于javascript而言，很好的保护了知识产权，因为不会涉及用户需要将代码提前下载的情况。
*   flask作为一款轻量的网站框架，可以很好地结合python优势，将算法以应用的方式呈现出来。
*   Django作为一种使用python实现的网络服务框架，与同样适用python实现的tornado和flask不一样，使用了完全独立的WSGI技术，并且可以轻松地分配路由，控制访问，并且由于使用python实现，可以轻松完成逻辑算法方面的内容。
*   作为服务部署算法可以很好地将网站压力分离开来。也就是应用服务器可以与网页服务器分割开来，很好地增强了安全性，也提高了服务体系任务分配的能力。通过将应用服务化后，可以更好的优化应用服务的QoS，并且在维护与调试应用时不会因为应用中断而影响网页服务。