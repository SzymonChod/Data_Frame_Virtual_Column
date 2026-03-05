import re
import pandas as pd
import operator


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Adds columns to the DataFrame based on simple mathemtical expressions. Doesn't allow division.

    :param df: Input DataFrame
    :param role: The mathematical expression in the format "name1 sign name2"
    :param new_column: Name of the new column to be added
    :return: If valid, returns a modified DataFrame, if not returns an empty DataDrame
    """

    # Checks if the expression is in correct format. Both wrong sign and names return an empty DataFrame
    if not re.fullmatch(r"[A-Za-z_\s\+\-\*]+", role):
        return pd.DataFrame()

    tokens = re.split(r"\s*([\+\-\*])\s*", role)

    # Checks if the expression consists of 3 tokens. Returns an empty DataFrame if not.
    if len(tokens) != 3:
        return pd.DataFrame()

    col1, op, col2 = [t.strip() for t in tokens]

    # Checks if columns exist in the given dataframe. Returns an empty DataFrame if not.
    if col1 not in df.columns or col2 not in df.columns:
        return pd.DataFrame()

    # Checks if the new column name is in correct format. Returns an empty DataFrame if not.
    if not re.fullmatch("[A-Za-z_]+", new_column):
        return pd.DataFrame()

    # Defines the 'op' token as mathematical operations
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
    }

    # If all is correct, adds the new column based on the expression
    try:
        df[new_column] = operations[op](df[col1], df[col2])
    except (TypeError, ValueError, KeyError) as e:
        return pd.DataFrame()

    return df
