"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.13
"""



import pandas as pd
from sklearn.model_selection import train_test_split
# PCA
from sklearn.decomposition import PCA

# This function merges two DataFrames on the 'stay' column.
def merge_revenue_stay(
    revenue: pd.DataFrame, 
    stay: pd.DataFrame
) -> pd.DataFrame:
    """Merges two DataFrames on the 'stay' column.

    Args:
        data (pd.DataFrame): The first DataFrame to merge.
        revenue (pd.DataFrame): The second DataFrame to merge.

    Returns:
        pd.DataFrame: Merged DataFrame.
    """
    data = pd.merge(revenue, stay, on=["Profile_id", 'CreatedOn', 'Reservation_clave', 'HotelId'],  how="inner")
    data = data[data["RevenueType"] == 9]
    # Filtra los datos por los outliers, me dieron un codigo de ejemplo, por favor aplicalo
    data = data[
        #(data['Nights'] <= data['Nights'].quantile(0.999)) &
        #(data['Nights'] > 0) #&
        (data['USDAmount'] >= data['USDAmount'].quantile(0.0005)) &
        (data['USDAmount'] <= data['USDAmount'].quantile(0.9995)) 
    ]
    return data

# A dimensionality reduction function using PCA.
def reduce_dimentionality(
    data: pd.DataFrame
) -> pd.DataFrame:
    """Reduces the dimensionality of the DataFrame using PCA.

    Args:
        data (pd.DataFrame): The DataFrame to reduce.

    Returns:
        pd.DataFrame: DataFrame with reduced dimensions and ignoring the old data.
    """
    # First standardize the data if necessary
    data = (data - data.mean()) / data.std()
    pca = PCA(n_components=5)  # Adjust n_components as needed
    reduced_data = pca.fit_transform(data.select_dtypes(include=[float, int]))
    reduced_df = pd.DataFrame(reduced_data, columns=[f'PC{i+1}' for i in range(reduced_data.shape[1])])
    return reduced_df

# This function splits the DataFrame into training and testing sets.
def split_data(
    data: pd.DataFrame, 
    test_size: float = 0.2, 
    random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the DataFrame into training and testing sets.

    Args:
        data (pd.DataFrame): The DataFrame to split.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Controls the shuffling applied to the data before applying the split.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Training and testing DataFrames.
    """
    return train_test_split(data, test_size=test_size, random_state=random_state
)

# Variable selection function that selects specific columns from the DataFrame.
def select_variables(
    data: pd.DataFrame, 
    variables: dict[str, list[str]]
) -> pd.DataFrame:
    """Selects specific columns from the DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame to select variables from.
        variables (list[str]): List of column names to select.

    Returns:
        pd.DataFrame: DataFrame with selected variables.
    """
    # Filtrar para que en RevenueType solo haya 9
    
    return data[variables["filtered"]]