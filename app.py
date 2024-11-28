# app.py

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from utils.data_loader import load_csv
from utils.schema_extractor import extract_schema
from utils.summary_generator import generate_summary
from agents.query_generator import generate_pandas_query
from agents.response_generator import generate_final_response
# from agents.visualizer import generate_matplotlib_code, save_plot
from fastapi.middleware.cors import CORSMiddleware

import os
import logging
from rich.console import Console

console = Console()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATA_DIR = "data"


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    file_location = f"{DATA_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    logger.info(f"File '{file.filename}' saved at '{file_location}'")
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.post("/ask_question/")
async def ask_question(question: str = Form(...), filename: str = Form(...)):
    
    logger.info(f"Received question: '{question}' for file: '{filename}'")
    # Load Data
    df = load_csv(f"{DATA_DIR}/{filename}")
    _vars = {}
    _vars["df"] = df
    _vars['query_result'] = None
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
    try:
        exec(pandas_query, _vars)
        query_result = _vars['query_result']
        console.log(query_result)
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

from agents.visualizer import generate_plotly_code, save_plot

@app.post("/visualize/")
async def visualize(question: str = Form(...), filename: str = Form(...)):
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

    # Save Plot
    plot_filename = save_plot(plotly_code, df)

    if not plot_filename:
        logger.error("Failed to generate the plot.")
        return JSONResponse(
            content={"error": "Failed to generate the plot."},
            status_code=400,
        )

    logger.info(f"Generated plot saved as: {plot_filename}")

    return FileResponse(plot_filename, media_type="image/png")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    uvicorn.run(app, host="0.0.0.0", port=8000)
