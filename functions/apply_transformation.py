import pandas as pd
import numpy as np


def apply_transformation(df, column, method):
    if method == "Normal":
        # No transformation needed, return the DataFrame as is
        return df
    elif method == "ln(x)":
        # Apply natural logarithm to the column
        df[column] = np.log(df[column])
    elif method == "x^2":
        # Square the values in the column
        df[column] = df[column] ** 2
    elif method == "√x":
        # Take the square root of the values in the column
        df[column] = np.sqrt(df[column])
    elif method == "∛x":
        # Take the cube root of the values in the column
        df[column] = np.cbrt(df[column])
    elif method == "e^x":
        # Take the exponential of the values in the column
        df[column] = np.exp(df[column])
    elif method == "1/x":
        # Take the reciprocal of the values in the column
        df[column] = 1 / df[column]
    elif method == "arcsin(√x)":
        # Apply the inverse sine function to the square root of the values in the column
        df[column] = np.arcsin(np.sqrt(df[column]))
    elif method == "x -> rank(x)":
        # Replace the values in the column with their rank
        df[column] = df[column].rank()
    else:
        # If an invalid method is provided, return the original DataFrame
        return df

    return df