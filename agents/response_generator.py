# agents/response_generator.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import logging
from rich.console import Console

console = Console()
load_dotenv()

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Initialize the OpenAI LLM with LangChain
llm = ChatOpenAI(temperature=0.5, model_name="gpt-4o-mini")

def generate_final_response(question, query_result, summary):
    logger.info("Generating final response.")
    prompt = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            """
            You are an AI assistant. Given the user's question, the query result, and a summary of the dataset, provide a concise and helpful answer.
                Query Result:
                {query_result}

                Dataset Summary:
                {summary}

                Answer:
            """,
        ),
        ("human", "{question}"),
        ]
    )


    chain = prompt | llm 
    _input = {
        "question": question,
        "query_result": str(query_result),
        "summary": summary
    }
    response = chain.invoke(_input)

    logger.debug(f"LLM response: {response.content}")

    final_response = response.content
    logger.info("Final response generated.")
    return final_response
