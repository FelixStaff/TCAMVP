"""
This is a boilerplate pipeline 'data_analysis'
generated using Kedro 0.19.13
"""
import sklearn as sk
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
import pandas as pd
from typing import Dict
# Recive a DataFrame and return a DataFrame with cluster labels
def make_cluster(
        merged_data: pd.DataFrame,
        cluster_params: Dict = None,
    ) -> pd.DataFrame:
    """Performs KMeans clustering on the 'merged_data' DataFrame.
    Args:
        merged_data (pd.DataFrame): The DataFrame containing the data to be clustered.
    Returns:
        pd.DataFrame: A DataFrame with the original data and an additional 'cluster' column.
    """
    # Extract features for clustering in Adults and Minors variables
    data = merged_data.values
    # Initialize KMeans with specified number of clusters and random state
    gmm = GaussianMixture(
        n_components=cluster_params["n_clusters"],
        random_state=cluster_params["random_state"]
    )
    # Fit the KMeans model to the data
    gmm.fit(data)
    # Predict cluster labels for the data
    labels = gmm.predict(data)
    # Create a new DataFrame with only the cluster labels
    return pd.DataFrame(labels, columns=["cluster"], index=merged_data.index)

def merge_data(
    data: pd.DataFrame, 
    clustered_data: pd.DataFrame
) -> pd.DataFrame:
    """Merges the original data with the clustered data.

    Args:
        data (pd.DataFrame): The original data.
        clustered_data (pd.DataFrame): The clustered data.

    Returns:
        pd.DataFrame: Merged DataFrame with cluster labels.
    """
    # Merge the original data with the clustered data on index
    return pd.merge(data, clustered_data, left_index=True, right_index=True)

# Function that separate and split the data
def split_data(
    data: pd.DataFrame, 
    params: Dict = None,
) -> list[pd.DataFrame]:
    """Splits the data into training and testing sets.

    Args:
        data (pd.DataFrame): The DataFrame to be split.
        train_size (float): Proportion of the dataset to include in the train split.

    Returns:
        Dict[str, pd.DataFrame]: Dictionary containing 'train' and 'test' DataFrames.

    Specifications:
    - The prediction is the cluster label.
    - The data is split into training and testing sets based on the specified train_size.
    """
    # Split the data into training and testing sets
    train_data, test_data = train_test_split(data, train_size=params["test_size"], random_state=params["random_state"])
    # Return the split data as a dictionary
    return train_data, test_data

# Visualization of the clusters and return the data with cluster labels
def plot_revenue_by_cluster(
    data: pd.DataFrame
):
    """Creates and saves a bar plot of revenue by cluster."""
    import matplotlib.pyplot as plt
    if 'cluster' not in data.columns or 'revenue' not in data.columns:
        raise ValueError("Data must contain 'cluster' and 'revenue' columns.")
    cluster_revenue = data.groupby('cluster')['revenue'].sum()
    fig, ax = plt.subplots()
    cluster_revenue.plot(kind='bar', ax=ax)
    ax.set_title('Total Revenue by Cluster')
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Total Revenue')
    plt.tight_layout()
    return fig

# Lets make the means of 