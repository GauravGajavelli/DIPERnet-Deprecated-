
import pandas as pd
import re
from zipfile import ZipFile
import os
import numpy as np

filedir = 'temp'
# with ZipFile('alltsv_csvfilesedgelistsandnodelabels.zip', 'r') as zipObj:
#    # Extract all the contents of zip file in current directory
#    zipObj.extractall(filedir)

controlFiles = [];
pdFiles = [];

directory = os.fsencode(filedir)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    # isControl = re.findall("(Control_Subject)+([0-9]{3})+(_164Nodes\.csv)",filename)
    isControl = re.findall("(Control_Subject)+([0-9]{3})+(_164Nodes).",filename)
    # isPD = re.findall("(PD_Subject)+([0-9]{3})+(_164Nodes\.csv)",filename)
    isPD = re.findall("(PD_Subject)+([0-9]{3})+(_164Nodes).",filename)
    if (len(isControl) > 0):
        controlFiles.append(filename)
    elif (len(isPD) > 0):
        pdFiles.append(filename)
    isControl = ''
    isPD = ''


a_filename = 'GCN_A.txt'
edge_labels_filename = 'GCN_edge_labels.txt'
graph_indicator_filename = 'GCN_graph_indicator.txt'
graph_labels_filename = 'GCN_graph_labels.txt'
node_labels_filename = 'GCN_node_labels.txt'

node_label_list_df = pd.read_csv(filedir + '/' + 'node labels.txt',header=None)

node_list = []

node_range = range(1,164)
for i in node_range:
    node_list.append(i);

nodes_df = pd.DataFrame(node_list, columns=["nodes"])

graphIndicator = 1
nodeIterator = 0
controlLabel = -1
pdLabel = 1
ctrlFile = controlFiles[0];
df = pd.read_csv(filedir+'/'+ctrlFile)
df['Source'] = df['Source'] + 164*nodeIterator
df['Target'] = df['Target'] + 164*nodeIterator
edgeList = df[['Source','Target']]
edgeFrames = [edgeList]

df['Edge_Labels'] = 1
edgeLabels = df['Edge_Labels']
edgeLabelsFrames = [edgeLabels]

node_label_frames = [node_label_list_df]

node_id_frames = [nodes_df]

graphIndicator_df = pd.DataFrame(index=np.arange(164))
graphIndicator_df['Graph Indicator'] = graphIndicator
graphIndicators = graphIndicator_df['Graph Indicator']

graphIndicatorFrames = [graphIndicators]

graphLabels_df = pd.DataFrame(index=np.arange(164))
graphLabels_df['Graph Label'] = controlLabel
graphLabels = graphLabels_df['Graph Label']
graphLabelFrames = [graphLabels]

nodeIterator += 1
graphIndicator += 1

for ctrlFile in controlFiles[1:]:
    df1 = pd.read_csv(filedir + '/' + ctrlFile)
    df1['Source'] = df1['Source'] + 164*nodeIterator
    df1['Target'] = df1['Target'] + 164*nodeIterator
    edgeList1 = df1[['Source','Target']]
    edgeFrames.append(edgeList1)

    df1['Edge_Labels'] = 1
    edgeLabels1 = df1['Edge_Labels']
    edgeLabelsFrames.append(edgeLabels1)
    node_label_frames.append(node_label_list_df)
    node_id_frames.append(nodes_df)

    graphIndicator_df1 = pd.DataFrame(index=np.arange(164))
    graphIndicator_df1['Graph Indicator'] = graphIndicator
    graphIndicators1 = graphIndicator_df1['Graph Indicator']
    graphIndicatorFrames.append(graphIndicators1)

    graphLabels_df1 = pd.DataFrame(index=np.arange(164))
    graphLabels_df1['Graph Label'] = controlLabel
    graphLabels1 = graphLabels_df1['Graph Label']
    graphLabelFrames.append(graphLabels1)
    
    nodeIterator += 1
    graphIndicator += 1



for pdFile in pdFiles:
    df1 = pd.read_csv(filedir + '/' + pdFile)
    df1['Source'] = df1['Source'] + 164*nodeIterator
    df1['Target'] = df1['Target'] + 164*nodeIterator
    edgeList1 = df1[['Source','Target']]
    edgeFrames.append(edgeList1)

    df1['Edge_Labels'] = 1
    edgeLabels1 = df1['Edge_Labels']
    edgeLabelsFrames.append(edgeLabels1)
    node_label_frames.append(node_label_list_df)
    node_id_frames.append(nodes_df)

    graphIndicator_df1 = pd.DataFrame(index=np.arange(164))
    graphIndicator_df1['Graph Indicator'] = graphIndicator
    graphIndicators1 = graphIndicator_df1['Graph Indicator']
    graphIndicatorFrames.append(graphIndicators1)

    graphLabels_df1 = pd.DataFrame(index=np.arange(164))
    graphLabels_df1['Graph Label'] = pdLabel
    graphLabels1 = graphLabels_df1['Graph Label']
    graphLabelFrames.append(graphLabels1)
    
    nodeIterator += 1
    graphIndicator += 1

edges_dfs = pd.concat(edgeFrames,ignore_index=True)
edges_dfs.to_csv(a_filename,header=False,index=False)

edgeLabelsDfs = pd.concat(edgeLabelsFrames,ignore_index=True)
edgeLabelsDfs.to_csv(edge_labels_filename,header=False,index=False)

nodeLabelDfs = pd.concat(node_label_frames,ignore_index=True)
nodeLabelDfs.to_csv(node_labels_filename,header=False,index=False)

graphIndicatorDfs = pd.concat(graphIndicatorFrames,ignore_index=True)
graphIndicatorDfs.to_csv(graph_indicator_filename,header=False,index=False)

graphLabelsDfs = pd.concat(graphLabelFrames,ignore_index=True)
graphLabelsDfs.to_csv(graph_labels_filename,header=False,index=False)