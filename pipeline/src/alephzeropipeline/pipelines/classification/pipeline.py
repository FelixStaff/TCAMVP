"""
This is a boilerplate pipeline 'classification'
generated using Kedro 0.19.13
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import training, create_model  # noqa

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=create_model,
            inputs="params:net_params",
            outputs="model_net",
            name="create_model_node",
        ),
        node(
            func=training,
            inputs=["train_data", "test_data", "model_net"],
            outputs="trained_net",
            name="training",
        )
        
    ])
