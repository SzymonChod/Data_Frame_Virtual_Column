import re
import pandas as pd
import operator


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Adds columns to the DataFrame based on simple mathemtical expressions. Doesn't allow division.

    :param df: Input DataFrame with 2 columns
    :param role: The mathematical expression in the format "name1 opperand name2"
    :param new_column: Name of the new column to be added
    :return: If valid, returns a modified DataFrame, if not returns an empty dataframe
    """

    # Checks if the expression is in correct format. Both wrong operands and names return an empty dataframe
    if not re.fullmatch(r"[A-Za-z_\s\+\-\*]+", role):
        return pd.DataFrame()

    tokens = re.split(r"\s*([\+\-\*])\s*", role)

    # Checks if the expression consists of 3 tokens. Returns an empty dataframe if not.
    if len(tokens) != 3:
        return pd.DataFrame()

    col1, op, col2 = [t.strip() for t in tokens]

    # Checks if columns exist in the given dataframe. Returns an empty dataframe if not.
    if col1 not in df.columns or col2 not in df.columns:
        return pd.DataFrame()

    # Checks if the new column name is in correct format. Returns an empty dataframe if not.
    if not re.fullmatch("[A-Za-z_]+", new_column):
        return pd.DataFrame()

    # Defines the 'op' token as mathematical operands
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
    }

    try:
        df[new_column] = operations[op](df[col1], df[col2])
    except (TypeError, ValueError, KeyError) as e:
        print(f"Failed to compute virtual column: {e}")
        return pd.DataFrame()

    return df
