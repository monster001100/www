#coding:utf-8
import os
import matplotlib
# 没有图形界面（如服务器）时使用 Agg 后端，只保存图片不弹窗
if os.name != 'nt' and not os.environ.get('DISPLAY') and not os.environ.get('MPLBACKEND'):
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import mpl
# 依次尝试常见中文字体（Windows: SimHei / macOS: PingFang SC / Linux: 文泉驿、Noto CJK）
mpl.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'Heiti SC',
                                   'WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', \
                            xytext=centerPt, textcoords='axes fraction', \
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args,
                            fontsize=plotTree.fontsize)

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = getTreeDepth(secondDict[key]) + 1
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, fontsize=plotTree.fontsize, color='blue')

def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalw, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalw
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

def _drawTree(inTree, fignum, title, save_path=None):
    """绘制决策树；save_path 不为空时保存为图片，有图形界面时同时弹窗显示。"""
    if isinstance(inTree, dict):
        numLeafs, depth = getNumLeafs(inTree), getTreeDepth(inTree)
    else:  # 整棵树被剪枝为单个叶节点
        numLeafs, depth = 1, 0
    # 按叶节点数和深度自适应画布大小与字号
    width = max(8.0, numLeafs * 1.1)
    height = max(5.0, (depth + 1) * 1.4)
    plotTree.fontsize = 10 if numLeafs <= 15 else 8
    fig = plt.figure(fignum, facecolor='white', figsize=(width, height))
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    if isinstance(inTree, dict):
        plotTree.totalw = float(numLeafs)
        plotTree.totalD = float(depth)
        plotTree.xOff = -0.5 / plotTree.totalw
        plotTree.yOff = 1.0
        plotTree(inTree, (0.5, 1.0), '')
    else:
        createPlot.ax1.text(0.5, 0.5, str(inTree), va="center", ha="center", bbox=leafNode,
                            fontsize=14, transform=createPlot.ax1.transAxes)
    plt.title(title, fontsize=14, color='red', pad=24)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print("决策树图片已保存到:", save_path)
    if matplotlib.get_backend().lower() != 'agg':
        plt.show()
    plt.close(fig)

def createPlot(inTree):
    _drawTree(inTree, 1, "决策树")

#ID3决策树
def ID3_Tree(inTree, title_suffix='', save_path=None):
    _drawTree(inTree, 1, "ID3决策树" + title_suffix, save_path)

#C4.5决策树
def C45_Tree(inTree, title_suffix='', save_path=None):
    _drawTree(inTree, 2, "C4.5决策树" + title_suffix, save_path)

#CART决策树
def CART_Tree(inTree, title_suffix='', save_path=None):
    _drawTree(inTree, 3, "CART决策树" + title_suffix, save_path)
