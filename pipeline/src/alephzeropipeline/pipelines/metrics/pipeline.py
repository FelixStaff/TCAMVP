"""
This is a boilerplate pipeline 'metrics'
generated using Kedro 0.19.13
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from .nodes import calcular_curva_roc, calcular_matriz_confusion, graficar_pie_beneficios_por_cluster, graficar_pie_poblacion_por_cluster, graficar_tabla_medias_clusters  # noqa

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=calcular_matriz_confusion,
            inputs=["trained_net", "test_data"],
            outputs="confusion_matrix",
            name="confusion_matrix_node",
        ),
        node(
            func=graficar_pie_beneficios_por_cluster,
            inputs=["final_data"],
            outputs="grafico_pie_beneficios",
            name="graficar_pie_beneficios_por_cluster_node",
        ),
        node(
            func=graficar_pie_poblacion_por_cluster,
            inputs=["final_data"],
            outputs="grafico_pie_poblacion",
            name="graficar_pie_poblacion_por_cluster_node",
        ),
        node(
            func=graficar_tabla_medias_clusters,
            inputs=["final_data"],
            outputs="grafico_tabla_medias",
            name="graficar_tabla_medias_clusters_node",
        ),
    ])
