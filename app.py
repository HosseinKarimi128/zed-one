# app.py

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.data_loader import load_csv
from utils.schema_extractor import extract_schema
from utils.summary_generator import generate_summary
from agents.query_generator import generate_pandas_query
from agents.response_generator import generate_final_response
from agents.visualizer import generate_plotly_code, get_plotly_json

import os
import logging
from rich.console import Console

console = Console()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for all origins (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"

# Ensure the data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file.
    """
    file_location = f"{DATA_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    logger.info(f"File '{file.filename}' saved at '{file_location}'")
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.post("/ask_question/")
async def ask_question(question: str = Form(...), filename: str = Form(...)):
    """
    Endpoint to ask a question about the uploaded CSV data.
    Generates a pandas query and returns a response based on the query result.
    """
    logger.info(f"Received question: '{question}' for file: '{filename}'")

    # Load Data
    df = load_csv(f"{DATA_DIR}/{filename}")
    if df is None:
        logger.error("Failed to load dataframe.")
        return JSONResponse(
            content={"error": "Failed to load the dataframe."},
            status_code=400,
        )

    # Extract Schema
    schema = extract_schema(df)

    # Generate Summary
    summary = generate_summary(df)

    # Generate Pandas Query
    pandas_query = generate_pandas_query(question, schema)

    if not pandas_query:
        logger.error("Failed to generate a valid pandas query.")
        return JSONResponse(
            content={"error": "Failed to generate a valid pandas query."},
            status_code=400,
        )

    # Execute Query
    _vars = {"df": df}
    try:
        exec(pandas_query, _vars)
        query_result = _vars.get('query_result', None)
        if query_result is None:
            raise ValueError("The generated query did not assign a value to 'query_result'.")
        logger.info("Successfully executed pandas query.")
    except Exception as e:
        logger.error(f"Failed to execute query: {e}")
        return JSONResponse(
            content={"error": f"Failed to execute query: {e}"},
            status_code=400,
        )

    # Generate Final Response
    final_response = generate_final_response(question, query_result, summary)

    logger.info(f"Generated response: {final_response}")

    return {"response": final_response}


@app.post("/visualize/")
async def visualize(question: str = Form(...), filename: str = Form(...)):
    """
    Endpoint to generate a Plotly visualization based on the user's question.
    Returns the Plotly figure in JSON format for interactive rendering on the frontend.
    """
    logger.info(f"Received visualization request: '{question}' for file: '{filename}'")

    # Load Data
    df = load_csv(f"{DATA_DIR}/{filename}")

    if df is None:
        logger.error("Failed to load dataframe.")
        return JSONResponse(
            content={"error": "Failed to load the dataframe."},
            status_code=400,
        )

    # Extract Schema
    schema = extract_schema(df)

    # Generate Plotly Code
    plotly_code = generate_plotly_code(question, schema)

    if not plotly_code:
        logger.error("Failed to generate Plotly code.")
        return JSONResponse(
            content={"error": "Failed to generate Plotly code."},
            status_code=400,
        )

    # Get Plotly JSON
    plotly_json = get_plotly_json(plotly_code, df)

    if not plotly_json:
        logger.error("Failed to generate Plotly JSON.")
        return JSONResponse(
            content={"error": "Failed to generate Plotly JSON."},
            status_code=400,
        )

    logger.info("Plotly JSON generated successfully.")

    return JSONResponse(content={"plotly_json": plotly_json})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
