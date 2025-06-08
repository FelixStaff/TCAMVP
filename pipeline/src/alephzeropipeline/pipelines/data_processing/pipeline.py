"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.13
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import merge_revenue_stay,reduce_dimentionality, select_variables  # noqa

__flow__ = [
    "data_processing",
    "classification",
    "data_analysis",
]

def create_pipeline(**kwargs) -> Pipeline:
    """Creates a Kedro pipeline for data processing.

    Returns:
        Pipeline: A Kedro pipeline object containing the data processing nodes.
    """
    return pipeline(
        [
            node(
                func=merge_revenue_stay,
                inputs=["revenue_dataset", "stay_dataset"],
                outputs="merged_data",
                name="csv_to_parquet_node",
            ),
            node(
                func=select_variables,
                inputs=["merged_data", "params:variables_selected"],
                outputs="filtered_data",
                name="filtered_data_node",
            ),
            node(
                func=reduce_dimentionality,
                inputs="filtered_data",
                outputs="reduced_data",
                name="reduce_dimentionality_node",
            ),
        ]
    )
