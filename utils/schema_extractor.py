# utils/schema_extractor.py

import logging
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

def extract_schema(df):
    logger.info("Extracting schema from dataframe.")
    schema = ""
    for column in df.columns:
        dtype = df[column].dtype
        schema += f"Column: {column}, Type: {dtype}\n"
    schema = schema.strip()
    logger.debug(f"Extracted schema: {schema}")
    return schema
