from django.test import TestCase

# Create your tests here.

from pyecharts.charts import *
from pyecharts import options as opts
import json
import os

def graph_les_miserables():
    with open(
            os.path.join("D:/","gms","static","json", "all_nodes.json"), "r", encoding="utf-8"
    ) as f:
        j = json.load(f)
        nodes = j["nodes"]
        links = j["links"]
        categories = j["categories"]

    graph = (
        Graph(init_opts=opts.InitOpts(width="1000px", height="1000px"))
        .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout=None,
            edge_label=['arrow'],
            repulsion=30,
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts(curve=0.3,opacity=0.7),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="kinship cluster map"),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_left="2%", pos_top="20%"
            ),
        )
    )
    graph.render('all1.html')

if __name__ == '__main__':
    graph_les_miserables()

