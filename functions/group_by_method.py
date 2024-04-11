import pandas as pd


def group_by_method(df, column, method):

    if method == "Mean":
        # Group by the specified column and calculate the mean of each group
        grouped_df = df.groupby(column).mean()
    elif method == "Median":
        # Group by the specified column and calculate the median of each group
        grouped_df = df.groupby(column).median()
    elif method == "Mode":
        # Group by the specified column and calculate the mode of each group
        grouped_df = df.groupby(column).agg(lambda x: x.mode().iloc[0])
    elif method == "First variable":
        # Group by the specified column and select the first variable in each group
        grouped_df = df.groupby(column).first()
    elif method == "Last variable":
        # Group by the specified column and select the last variable in each group
        grouped_df = df.groupby(column).last()
    else:
        # If an invalid method is provided, return None
        return df

    return grouped_df