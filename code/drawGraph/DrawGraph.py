import os
import numpy as np
from skimage.measure import regionprops, label, find_contours
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import networkx as nx

from drawGraph.DrawGraphSettings import DrawGraphSetting


class DrawGraph:
    def __init__(self):
        self.settings = DrawGraphSetting()
        self.rawImgs = os.listdir(self.settings.rawPath)
        self.maskImgs = os.listdir(self.settings.maskPath)

    def draw_graph(self):
        def calculate_scale():
            # 1 inch = 0.0254 meter
            scale_target = self.settings.scaleTarget / 0.0254  # inch
            dots_in_scale = scale_target * self.settings.dpi / self.settings.scanMag
            return dots_in_scale

        def draw_graph_on_mask():
            plt.figure(figsize=(img_width / self.settings.dpi, img_len / self.settings.dpi),
                       dpi=self.settings.dpi)
            plt.imshow(mask_img, plt.cm.gray)
            nx.draw_networkx_nodes(graph, pos, node_size=node_size,
                                   node_color='b', alpha=0.5, edgecolors='r')
            nx.draw_networkx_edges(graph, pos, width=6, alpha=1, edge_color='white')
            nx.draw_networkx_labels(graph, pos)
            plt.scatter(px, py, color='white', s=5)
            plt.text((px[0] + px[1]) / 2, (py[0] + py[1]) / 2, self.settings.scaleStr,
                     ha='center', color='white', fontsize=15)
            plt.plot(px, py, color='white')
            plt.savefig(self.settings.maskGraphPath + imgName.split(".")[0] + "GraphOnMask.png")

        def draw_graph_on_raw():
            plt.figure(figsize=(img_width / self.settings.dpi, img_len / self.settings.dpi),
                       dpi=self.settings.dpi)
            plt.axis('off')
            plt.imshow(raw_img)
            for n, contour in enumerate(contours):
                plt.plot(contour[:, 1], contour[:, 0], linewidth=3, color='b')
            nx.draw_networkx_edges(graph, pos, width=2, edge_color='k')
            plt.scatter(px, py, color='b', s=5)
            plt.text((px[0]+px[1])/2, (py[0]+py[1])/2, self.settings.scaleStr,
                     ha='center', color='b', fontsize=15)
            plt.plot(px, py, color='b')
            plt.savefig(self.settings.rawGraphPath + imgName.split(".")[0] + "GraphOnRaw.png")

        def generate_graph():
            def generate_nodes():
                for i in range(len(props)):
                    temp = props[i]
                    pos[i] = (temp.centroid[1], temp.centroid[0])
                    node_size.append(temp.area)
                    graph.add_node(i, area=temp.area, pos=(temp.centroid[1], temp.centroid[0]),
                                   rad=temp.equivalent_diameter / 2)

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
                raw_img = plt.imread(os.path.join(self.settings.rawPath, imgName))
                mask_img = plt.imread(os.path.join(self.settings.maskPath, imgName), plt.cm.gray)
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
                scale_dots = calculate_scale()
                py = [100, 100]
                px = [100, 100 + scale_dots]
                contours = find_contours(mask_img, 0.5)
                draw_graph_on_mask()
                draw_graph_on_raw()

#     # 检测所有图形的轮廓
#     #
#
#     # # 绘制轮廓
#     # fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 8))
#     # ax0.imshow(img, plt.cm.gray)
#     # ax1.imshow(img, plt.cm.gray)
#     # for n, contour in enumerate(contours):
#     #     ax1.plot(contour[:, 1], contour[:, 0], linewidth=2)
#     # ax1.axis('image')
#     # ax1.set_xticks([])
#     # ax1.set_yticks([])
#     # plt.show()