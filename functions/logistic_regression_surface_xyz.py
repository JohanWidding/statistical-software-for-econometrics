import numpy as np
import pandas as pd
import statsmodels.api as sm


def logistic_regression_surface(df, dependent_var, explanatory_vars, time_control=None, entity_control=None,
                                cluster=None, sample_percentage=1):
    df = df.sample(frac=sample_percentage, random_state=42)
    # Extract dependent variable and explanatory variables from the DataFrame
    y = df[dependent_var]
    X = df[explanatory_vars]

    # Create dummy variables for time control
    if time_control is not None:
        dummy_time = pd.get_dummies(df[time_control], prefix='dummy', dtype=int)
        X = pd.concat([X, dummy_time], axis=1)

    # Create dummy variables for entity control
    if entity_control is not None:
        dummy_entity = pd.get_dummies(df[entity_control], prefix='dummy', dtype=int)
        X = pd.concat([X, dummy_entity], axis=1)

    # Add constant to the explanatory variables
    X = sm.add_constant(X)

    # Define and fit the logistic regression model
    model = sm.Logit(y, X)
    results = model.fit()

    # Cluster standard errors if specified
    if cluster is not None:
        results = model.fit(cov_type='cluster', cov_kwds={'groups': df[cluster]})

    # Generate meshgrid data for specified explanatory variables
    plot_data = []
    for var in explanatory_vars[:2]:
        plot_data.append(np.linspace(df[var].min(), df[var].max(), 50))

    meshgrid_data = np.meshgrid(*plot_data)

    X = meshgrid_data[0]
    Y = meshgrid_data[1]

    params_list = [results.params.tolist()]
    print(results.summary())
    # Convert list of arrays to 2D array
    Z = custom_predict_proba(params_list, X, Y)
    Z = Z.reshape(meshgrid_data[0].shape)

    return X, Y, Z

def custom_predict_proba(params_list, X, Y):
    """
    Calculate predicted probabilities using logistic regression equation.

    Args:
    - params_list (list of lists): Coefficients of the logistic regression model.
    - X (2D array): Meshgrid X data.
    - Y (2D array): Meshgrid Y data.

    Returns:
    - Z (2D array): Predicted probabilities.
    """
    # Apply logistic regression equation using coefficients
    intercept = 0  # Assuming no intercept for simplicity
    Z = []
    for i in range(len(X)):
        row = []
        for j in range(len(Y)):
            linear_pred = intercept
            linear_pred += params_list[0][1] * X[i][j] + params_list[0][2] * Y[i][j]  # Accessing each coefficient pair
            row.append(1 / (1 + np.exp(-linear_pred)))
        Z.append(row)

    return np.array(Z)