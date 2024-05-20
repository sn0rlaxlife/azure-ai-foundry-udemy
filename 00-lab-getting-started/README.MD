# 00-Lab-Getting-Started

## Description

This project is a step-by-step guide on how to set up a virtual environment in Python and install the requirements.

## Prerequisites

- Python (version 3.11.0 or higher) installed on your machine
- pip (Python package installer) installed on your machine

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/sn0rlaxlife/azure-ai-studio.git
    ```

2. Navigate to the project directory:

    ```bash
    cd 00-lab-getting-started
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - For Windows:

      ```bash
      venv\Scripts\activate
      ```

    - For macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

5. Install the project requirements:

    ```bash
    pip install -r requirements.txt
    ```

6. Set environment variables for use of Azure OpenAI Service

You can use the .env.example to set your own .env with the API keys and endpoint or you can run environment variables
    ```bash
    $env:AZURE_OPENAI_ENDPOINT='<your-endpoint>'
    $env:CHAT_COMPLETIONS_DEPLOYMENT_NAME='<name-of-deployment>'
    $env:AZURE_OPENAI_API_KEY='<api-key>'
    ```

7. ***IMPORTANT*** ensure that you run unset on environment variables after you complete this lab. For windows follow the Remove-Item and for MacOS you can run the unset.
   ```bash
   Remove-Item Env:<variable-name>
   ```
   ```bash
   unset <variable-name>
   ```

## Usage

1. Run the project:

    ```bash
    python main.py
    ```

2. Follow the on-screen instructions to interact with the application.

3. Test out a query you want to query, run both main.py with the commented portion to understand the difference of responses the first one cleans up the response to just return the response the second .to_json() will represent the raw response back to the terminal.


## License

This project is licensed under the [MIT License](LICENSE).