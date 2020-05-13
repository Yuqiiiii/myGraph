import os
import numpy as np
from skimage.measure import regionprops, label
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import networkx as nx
import sys

from drawGraph.DrawGraphSettings import DrawGraphSetting


class DrawGraph:
    def __init__(self):
        self.settings = DrawGraphSetting()
        self.rawPath = os.path.join(sys.path[0], self.settings.rawPath)
        self.maskPath = os.path.join(sys.path[0], self.settings.maskPath)
        self.rawGraphPath = os.path.join(sys.path[0], self.settings.rawGraphPath)
        self.maskGraphPath = os.path.join(sys.path[0], self.settings.maskGraphPath)
        self.rawImgs = os.listdir(self.rawPath)
        self.maskImgs = os.listdir(self.maskPath)

    def draw_graph(self):

        def draw_graph_on_mask():
            plt.figure(figsize=(img_width / self.settings.dpi, img_len / self.settings.dpi), dpi=self.settings.dpi)
            plt.imshow(mask_img, plt.cm.gray)
            nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color='b', alpha=0.5, edgecolors='r')
            nx.draw_networkx_edges(graph, pos, width=6, alpha=1, edge_color='white')
            nx.draw_networkx_labels(graph, pos)
            plt.savefig(self.maskGraphPath + imgName.split(".")[0] + "GraphOnMask.png")

        def draw_graph_on_raw():
            plt.figure(figsize=(img_width / self.settings.dpi, img_len / self.settings.dpi), dpi=self.settings.dpi)
            plt.imshow(raw_img)
            nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color='b', alpha=0.3, edgecolors='r')
            nx.draw_networkx_edges(graph, pos, width=3, alpha=0.5, edge_color='b')
            plt.savefig(self.rawGraphPath + imgName.split(".")[0] + "GraphOnRaw.png")

        def generate_graph():
            def generate_nodes():
                for i in range(len(props)):
                    temp = props[i]
                    pos[i] = (temp.centroid[1], temp.centroid[0])
                    node_size.append(temp.area)
                    graph.add_node(i, area=temp.area, pos=(temp.centroid[1], temp.centroid[0]), rad=temp.equivalent_diameter / 2)

            def generate_edges():
                x = np.array(list(pos.values()))
                nbrs = NearestNeighbors(n_neighbors=self.settings.K + 1, algorithm='ball_tree').fit(x)
                distances, indices = nbrs.kneighbors(x)
                for i in range(indices.shape[0]):
                    for j in range(1, indices.shape[1]):
                        graph.add_edge(i, indices[i, j], distance=indices[i, j])

            props = regionprops(label(mask_img))
            generate_nodes()
            generate_edges()

        for imgName in self.rawImgs:
            try:
                raw_img = plt.imread(os.path.join(self.rawPath, imgName))
                mask_img = plt.imread(os.path.join(self.maskPath, imgName), plt.cm.gray)
            except IOError:
                print(imgName + " cannot be processed! Please check if it is a valid image"
                                "and exists in both raw and mask folders!")
            else:
                # generate graph
                graph = nx.Graph()
                pos = {}
                node_size = []
                generate_graph()
                # draw graph
                img_len = mask_img.shape[0]
                img_width = mask_img.shape[1]
                draw_graph_on_mask()
                draw_graph_on_raw()
