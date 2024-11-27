# agents/visualizer.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import logging
from rich.console import Console

console = Console()
load_dotenv()

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Initialize the OpenAI LLM with LangChain
llm = ChatOpenAI(temperature=0.0, model_name="gpt-4o-mini")

def generate_matplotlib_code(question, schema):
    logger.info("Generating matplotlib code.")
    prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            """
            You are a data visualization expert. Based on the following schema and question, generate matplotlib code to visualize the data appropriately.
            Provide only the code between triple backticks. the user passed the dataframe as df variable, you should not read the csv the df is input.

            Schema:
            {schema}

            ```python
            # Matplotlib code here
            ```
            """,
        ),
        ("human", "{question}"),
        ]
    )

    chain = prompt | llm 
    _input = {"schema": schema, "question": question}
    
    response = chain.invoke(_input)

    logger.debug(f"LLM response: {response.content}")

    # Extract code between ```python and ```
    code = extract_code_block(response.content)

    logger.debug(f"Extracted code: {code}")

    return code.strip()

def extract_code_block(response):
    import re
    code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
    if code_match:
        code = code_match.group(1)
    else:
        code = response
    return code

def save_plot(code, df):
    logger.info("Saving plot.")
    # Prepare a namespace for exec
    namespace = {'df': df, 'plt': plt}
    try:
        exec(code, namespace)
        plot_filename = 'plot.png'
        plt.savefig(plot_filename)
        plt.close()
        logger.info(f"Plot saved as {plot_filename}")
        return plot_filename
    except Exception as e:
        logger.error(f"Error generating plot: {e}")
        return None
