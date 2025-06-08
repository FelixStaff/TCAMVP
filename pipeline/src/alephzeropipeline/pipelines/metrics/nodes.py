import numpy as np
from sklearn.metrics import roc_curve, auc
# Import the multilayer perceptron model from sklearn
from sklearn.neural_network import MLPClassifier
from pickle import load
import pandas as pd
from sklearn.metrics import confusion_matrix
"""
This is a boilerplate pipeline 'metrics'
generated using Kedro 0.19.13
"""
import matplotlib.pyplot as plt

clusters_name = {
    0: 'Personas Individuales',
    1: 'Parejas Sin Hijos',
    2: 'Familias Nucleares'
}

def calcular_curva_roc(
    model: MLPClassifier, 
    test_data: pd.DataFrame
    ) -> plt.Figure:
    """
    Calcula y grafica la curva ROC para un modelo de red neuronal cargado con Kedro.
    Convierte los valores de la columna 'cluster' a 1 si pudo predecir (éxito) y 0 si no pudo (fracaso).

    Args:
    model: Un objeto Kedro DataSet que contiene el modelo pickle.
    test_data: DataFrame con los datos de test, debe contener la columna 'cluster'.
    """

    # Convertir la columna 'cluster' a binaria: 1 si pudo, 0 si no pudo
    y_test = test_data["cluster"].apply(lambda x: 1 if x else 0)
    X_test = test_data.drop(columns=["cluster"])

    # Obtener probabilidades de predicción
    y_score = model.predict_proba(X_test)[:, 1]  # Probabilidades de la clase positiva

    # Calcular la curva ROC
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)

    # Graficar la curva ROC
    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver Operating Characteristic')
    ax.legend(loc="lower right")
    return fig

def calcular_matriz_confusion(
    model: MLPClassifier,
    test_data: pd.DataFrame
    ) -> plt.Figure:
    """
    Calcula y grafica la matriz de confusión (en porcentajes por clase) para un modelo de red neuronal cargado con Kedro.
    Convierte los valores de la columna 'cluster' a 1 si pudo predecir (éxito) y 0 si no pudo (fracaso).

    Args:
    model: Un objeto Kedro DataSet que contiene el modelo pickle.
    test_data: DataFrame con los datos de test, debe contener la columna 'cluster'.

    Returns:
    plt.Figure: Figura de matplotlib con la matriz de confusión en porcentajes por clase.
    """
    y_test = test_data["cluster"]
    X_test = test_data.drop(columns=["cluster", "LocalCurrencyAmount"])  # Excluir 'LocalCurrencyAmount' si no es relevante para la predicción
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    # Calcular porcentajes por clase (por fila)
    cm_percent = cm / cm.sum(axis=1, keepdims=True) * 100

    fig, ax = plt.subplots()
    im = ax.imshow(cm_percent, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xlabel='Predicted label',
        ylabel='True label',
        title='Confusion Matrix (%) por clase'
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    thresh = cm_percent.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            value = cm_percent[i, j]
            if np.isnan(value):
                display = "N/A"
            else:
                display = f"{value:.1f}%"
            ax.text(j, i, display,
                    ha="center", va="center",
                    color="white" if value > thresh else "black")
    fig.tight_layout()
    return fig

def graficar_pie_beneficios_por_cluster(
    final_data: pd.DataFrame
) -> plt.Figure:
    """
    Genera un gráfico de pastel mostrando la proporción de beneficios por cada clase de cluster,
    usando los nombres definidos en el diccionario clusters_name.

    Args:
    final_data: DataFrame con las columnas 'cluster' y 'USDAmount'.

    Returns:
    plt.Figure: Figura de matplotlib con el gráfico de pastel de beneficios por cluster.
    """
    beneficios_por_cluster = final_data.groupby("cluster")['LocalCurrencyAmount'].sum()
    labels = [clusters_name.get(idx, str(idx)) for idx in beneficios_por_cluster.index]
    total = beneficios_por_cluster.sum()
    porcentajes = beneficios_por_cluster / total * 100
    legend_labels = [f"{label} ({porcentaje:.1f}%)" for label, porcentaje in zip(labels, porcentajes)]
    colors = ['#b47e58', '#ca3e49', '#2f3650']
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        beneficios_por_cluster,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        counterclock=True,
        pctdistance=0.85,
        colors=colors[:len(beneficios_por_cluster)]
    )
    # Mostrar los porcentajes en el gráfico
    for autotext in autotexts:
        autotext.set_visible(True)
        autotext.set_fontsize(9)
    # Leyenda en la esquina superior derecha
    ax.legend(wedges, legend_labels, title="Clusters", loc="upper right", bbox_to_anchor=(1.25, 1), fontsize=9)
    ax.set_title("Distribución de beneficios por cluster")
    fig.tight_layout()
    return fig

def graficar_pie_poblacion_por_cluster(
    final_data: pd.DataFrame
) -> plt.Figure:
    """
    Genera un gráfico de pastel mostrando el porcentaje poblacional de cada clase de cluster,
    usando los nombres definidos en el diccionario clusters_name.

    Args:
    final_data: DataFrame con la columna 'cluster'.

    Returns:
    plt.Figure: Figura de matplotlib con el gráfico de pastel de población por cluster.
    """
    poblacion_por_cluster = final_data["cluster"].value_counts().sort_index()
    labels = [clusters_name.get(idx, str(idx)) for idx in poblacion_por_cluster.index]
    total = poblacion_por_cluster.sum()
    porcentajes = poblacion_por_cluster / total * 100
    legend_labels = [f"{label} ({porcentaje:.1f}%)" for label, porcentaje in zip(labels, porcentajes)]
    colors = ['#b47e58', '#ca3e49', '#2f3650']
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        poblacion_por_cluster,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        counterclock=False,
        pctdistance=0.85,
        colors=colors[:len(poblacion_por_cluster)]
    )
    for autotext in autotexts:
        autotext.set_visible(True)
        autotext.set_fontsize(9)
    # Leyenda en la esquina superior derecha
    ax.legend(wedges, legend_labels, title="Clusters", loc="upper right", bbox_to_anchor=(1.25, 1), fontsize=9)
    ax.set_title("Distribución poblacional por cluster")
    fig.tight_layout()
    return fig

def graficar_tabla_medias_clusters(
    final_data: pd.DataFrame
) -> plt.Figure:
    """
    Calcula y muestra una tabla con matplotlib mostrando las medias de variables por cluster,
    con orientación horizontal (clusters como filas, variables como columnas).

    Args:
    final_data: DataFrame con los datos originales, debe tener una columna 'cluster'.

    Returns:
    plt.Figure: Figura de matplotlib con la tabla de medias por cluster.
    """
    # Calcular medias por cluster, excluyendo 'ExchangeRate' si existe
    means = final_data.groupby('cluster').mean(numeric_only=True)
    if 'ExchangeRate' in means.columns:
        means = means.drop(columns=['ExchangeRate'])
    means = means.round(1)
    means.index.name = 'Cluster'
    # Reemplazar los índices numéricos por los nombres de clusters si existen
    cluster_labels = [clusters_name.get(idx, str(idx)) for idx in means.index]
    means.index = cluster_labels
    # Paleta de colores para filas
    row_colors = ['#b47e58', '#ca3e49', '#2f3650']
    fig_width = max(8, len(means.columns) * 1.5)
    fig_height = max(1.0, len(means.index) * 0.5)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=means.values,
        rowLabels=means.index,
        colLabels=means.columns,
        cellLoc='center',
        loc='center',
        rowColours=row_colors[:len(means.index)]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.title('Medias por Cluster')
    fig.tight_layout()
    return fig