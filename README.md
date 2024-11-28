# Data Analysis Assistant

An AI-powered data analysis assistant that allows users to upload CSV files, ask questions about their data, and receive insightful answers and visualizations. Built using FastAPI, LangChain, OpenAI's GPT models, and pandas, this application streamlines data exploration by generating pandas queries and matplotlib visualizations based on user input.

## Features

- **CSV Upload**: Upload your CSV files for analysis.
- **Natural Language Queries**: Ask questions about your data in plain English.
- **Automated Pandas Queries**: Generates efficient pandas queries based on your questions.
- **Data Summarization**: Provides summaries of your datasets.
- **Visualizations**: Generates matplotlib code to visualize your data based on your queries.
- **API Endpoints**: Accessible via RESTful API endpoints.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
    - [Upload CSV](#upload-csv)
    - [Ask a Question](#ask-a-question)
    - [Visualize Data](#visualize-data)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/data-analysis-assistant.git
cd data-analysis-assistant
```

## Setup

1. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   - Create a `.env` file in the root directory.
   - Add your OpenAI API key and any other necessary environment variables:

     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Create Data Directory**:

   - Ensure there's a `data` directory in the root folder where uploaded CSV files will be stored:

     ```bash
     mkdir data
     ```

## Usage

Run the FastAPI application:

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

#### 1. Upload CSV

- **URL**: `/upload_csv/`
- **Method**: `POST`
- **Description**: Upload a CSV file for analysis.
- **Form Data**:
  - `file`: The CSV file to upload.

**Example using `curl`**:

```bash
curl -X POST "http://localhost:8000/upload_csv/" \
  -F "file=@your_data.csv"
```

#### 2. Ask a Question

- **URL**: `/ask_question/`
- **Method**: `POST`
- **Description**: Ask a question about your data.
- **Form Data**:
  - `question`: The question in plain English.
  - `filename`: The name of the uploaded CSV file.

**Example using `curl`**:

```bash
curl -X POST "http://localhost:8000/ask_question/" \
  -F "question=What is the average sales in 2020?" \
  -F "filename=your_data.csv"
```

#### 3. Visualize Data

- **URL**: `/visualize/`
- **Method**: `POST`
- **Description**: Generate a visualization based on your question.
- **Form Data**:
  - `question`: The visualization request in plain English.
  - `filename`: The name of the uploaded CSV file.

**Example using `curl`**:

```bash
curl -X POST "http://localhost:8000/visualize/" \
  -F "question=Plot the sales trend over 2020" \
  -F "filename=your_data.csv" \
  --output plot.png
```

## Examples

### 1. Uploading a CSV File

```bash
curl -X POST "http://localhost:8000/upload_csv/" \
  -F "file=@sales_data.csv"
```

### 2. Asking a Question

```bash
curl -X POST "http://localhost:8000/ask_question/" \
  -F "question=Which product had the highest sales in Q1 2020?" \
  -F "filename=sales_data.csv"
```

**Sample Response**:

```json
{
  "response": "In Q1 2020, Product A had the highest sales."
}
```

### 3. Generating a Visualization

```bash
curl -X POST "http://localhost:8000/visualize/" \
  -F "question=Show a bar chart of sales by region for 2020" \
  -F "filename=sales_data.csv" \
  --output sales_by_region.png
```

This command will save the generated plot as `sales_by_region.png`.

## Dependencies

- Python 3.7+
- FastAPI
- Uvicorn
- pandas
- matplotlib
- OpenAI
- LangChain
- Rich
- python-dotenv

**Install all dependencies using**:

```bash
pip install -r requirements.txt
```

## Project Structure

```
├── app.py
├── agents
│   ├── query_generator.py
│   ├── response_generator.py
│   └── visualizer.py
├── utils
│   ├── data_loader.py
│   ├── schema_extractor.py
│   └── summary_generator.py
├── data
│   └── (uploaded CSV files)
├── .env
├── requirements.txt
└── README.md
```

- **app.py**: The main FastAPI application.
- **agents/**: Contains modules that interact with the language model to generate queries, responses, and visualizations.
- **utils/**: Utility modules for loading data, extracting schema, and generating summaries.
- **data/**: Directory to store uploaded CSV files.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for the powerful language models.
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework.
- [LangChain](https://langchain.com/) for simplifying LLM integrations.
- [pandas](https://pandas.pydata.org/) and [matplotlib](https://matplotlib.org/) for data manipulation and visualization.

---

Feel free to customize this README to better suit your project's needs.