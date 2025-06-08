"""
This is a boilerplate pipeline 'data_analysis'
generated using Kedro 0.19.13
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import make_cluster, merge_data, split_data, plot_revenue_by_cluster  # noqa

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=make_cluster,
            inputs=["reduced_data", "params:gmm_params"],
            outputs="clustered_data",
            name="make_cluster_node",
        ),
        node(
            func=merge_data,
            inputs=["filtered_data", "clustered_data"],
            outputs="final_data",
            name="merge_data_node",
        ),
        node(
            func=split_data,
            inputs=["final_data", "params:split_params"],
            outputs=["train_data", "test_data"],
            name="split_data_node",
        ),
        # node(
        #     func=plot_revenue_by_cluster,
        #     inputs="final_data",
        #     outputs="revenue_plot",
        #     name="plot_revenue_by_cluster_node",
        # ),
    ])
