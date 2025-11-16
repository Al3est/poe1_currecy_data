# Path of Exile Currency Data Pipeline

This project is a data pipeline designed to extract, process, and store currency exchange rate data from the game Path of Exile. It uses Apache Airflow to orchestrate the workflow and Docker to containerize the application for easy setup and deployment.

## Technology Stack

### Orchestration & Environment
- **Apache Airflow:** Core platform for authoring, scheduling, and monitoring data workflows.
- **Docker & Docker Compose:** Used to build and run the entire application environment in isolated containers.

### Data Storage
- **PostgreSQL:** Serves as the backend metadata database for Airflow and stores the final, processed currency data.
- **Amazon S3:** Used as a data lake to store the raw, unprocessed JSON data extracted from the API.
- **Redis:** Included in the environment as a message broker.

### Key Python Libraries
- **requests:** For making HTTP requests to the Path of Exile API.
- **pandas:** For all data manipulation and transformation tasks.
- **boto3:** The official AWS SDK for Python, used to upload data to S3.

## Workflow Overview

The main data pipeline is defined in the `orchestration.py` DAG. This workflow automates the process of fetching, cleaning, and storing currency data from Path of Exile. The process is broken down into several tasks, with each task's logic separated into utility scripts in the `include/` directory.

1.  **Extract Data (`api_utils.py`)**
    - The pipeline begins with a task that calls a function from `api_utils.py`.
    - This script makes an HTTP request to a public Path of Exile API (e.g., poe.ninja) to get the latest currency exchange rates.
    - The raw JSON response is then saved into the `rawdata/` directory for persistence and subsequent processing.

2.  **Transform Data (`transform_utils.py`)**
    - Following a successful extraction, a transformation task is triggered.
    - This task uses functions from `transform_utils.py` to read the raw JSON file from the `rawdata/` directory.
    - The script parses the data, cleans it by selecting only the relevant fields (like currency names and their values in Chaos Orbs), and structures it into a clean, tabular format.

3.  **Load Data (`storage_utils.py`)**
    - In the final step, the transformed, clean data is passed to a loading task.
    - This task utilizes a function from `storage_utils.py` to save the data for analysis or downstream use.
