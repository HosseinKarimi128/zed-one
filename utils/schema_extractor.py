# utils/schema_extractor.py

import logging
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

def extract_schema(df):
    logger.info("Extracting schema from dataframe.")
    schema = ""
    # add name of all columns to schema
    schema += "Name of data columns:\n"
    for column in df.columns:
        dtype = df[column].dtype
        schema += f"Column: {column}, Type: {dtype}\n"

    # extract numerical columns along with their dtype, mean and std
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
    schema += "Numerical columns along with their dtype, mean and std:\n"
    for column in numerical_columns:
        dtype = df[column].dtype
        mean = df[column].mean()
        std = df[column].std()
        schema += f"Column: {column}, Type: {dtype}, Mean: {mean}, Std: {std}\n"

    # extract categorical columns along with their dtype and unique values
    categorical_columns = df.select_dtypes(include=['object']).columns
    schema += "Categorical columns along with their dtype and unique values:\n"
    for column in categorical_columns:
        dtype = df[column].dtype
        unique_values = df[column].unique()
        schema += f"Column: {column}, Type: {dtype}, Unique Values: {unique_values}\n"

    # extract boolean columns along with their dtype and unique values
    boolean_columns = df.select_dtypes(include=['bool']).columns
    schema += "Boolean columns along with their dtype and unique values:\n"
    for column in boolean_columns:
        dtype = df[column].dtype
        unique_values = df[column].unique()
        schema += f"Column: {column}, Type: {dtype}, Unique Values: {unique_values}\n"

    # extract date columns along with their dtype and unique values
    date_columns = df.select_dtypes(include=['datetime64']).columns
    schema += "Date columns along with their dtype and unique values:\n"
    for column in date_columns:
        dtype = df[column].dtype
        unique_values = df[column].unique()
        schema += f"Column: {column}, Type: {dtype}, Unique Values: {unique_values}\n"

    schema = schema.strip()
    return schema
