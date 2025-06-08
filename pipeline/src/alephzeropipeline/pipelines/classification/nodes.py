"""
This is a boilerplate pipeline 'classification'
generated using Kedro 0.19.13
"""
# Load the neural network model
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pandas as pd


def create_model(
    model_params: dict
) -> MLPClassifier:
    """Creates a neural network model with the given parameters.

    Args:
        model_params (dict): Parameters for the MLPClassifier.

    Returns:
        MLPClassifier: An instance of the MLPClassifier with the specified parameters.
    """
    print ("Creating model with parameters:", model_params)
    # Make the hidden_layer_sizes a tuple if it's not already
    if isinstance(model_params.get('hidden_layer_sizes'), int):
        model_params['hidden_layer_sizes'] = list(
            model_params['hidden_layer_sizes']
        )
    return MLPClassifier(**model_params, max_iter=20)

def training(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    model : MLPClassifier,
) -> MLPClassifier:
    """Classifies the input data using a neural network model.
 
    Args:
        data (pd.DataFrame): The input data to classify.
        params (dict): Parameters for the classification model.

    Returns:
        pd.DataFrame: DataFrame with predictions added.
    """
    
    # Fit the model on the data
    X = train_data.drop(columns=['cluster', 'LocalCurrencyAmount'])  # Assuming 'target' is the label column
    y = train_data['cluster']
    

    model.fit(X, y)
    
    # Calculate accuracy on the test data
    X_test = test_data.drop(columns=['cluster','LocalCurrencyAmount'])  # Assuming 'target' is the label column
    y_test = test_data['cluster']
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {accuracy:.2f}")
    # Now print the number of correct predictions
    correct_predictions = (predictions == y_test).sum()
    print(f"Number of correct predictions: {correct_predictions}/ {len(y_test)}")
    
    
    return model

