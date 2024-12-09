## Promptflow with Exa.ai API ##
This is to demonstrate the use of a powerful search engine "Exa" and following a pattern flow via code using prompt-flow as the orchestrator.

# Installation

To install this Python package, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment using the command `python -m venv env`.
4. Activate the virtual environment:
    - On Windows: `.\env\Scripts\activate`
    - On macOS and Linux: `source env/bin/activate`
5. Install the required dependencies by running `pip install -r requirements.txt`.

# .env Variables

To use a `.env` file and ensure that sensitive information is not committed to version control, follow these steps:

1. Create a file named `.env` in the project directory.
2. Add the necessary environment variables to the `.env` file, each on a new line in the format `VARIABLE_NAME=VALUE`.
3. Make sure to include the `.env` file in your `.gitignore` to prevent it from being tracked by Git.

# Install requirements
```bash
pip install -r requirements.txt
```
Once these are installed we have to establish our connection with the LLM/Serverless Instance this is faciliated by the file openai.yml.example
Edit the values inside this file
```bash
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/AzureOpenAIConnection.schema.json
name: open_ai_connection
type: azure_open_ai
api_key: <api_key> # you can pass this via cli if you'd like
api_base: <base-url> # this is from the instance deployed
api_version: <api-version> # Version that is selected in the deployment model
api_type: azure # if using azure openai
```

# Establish connection once you have a file with your values (Add to .gitignore)
```bash
pf flow connection create --file=openai.yml
```

# Start the flow
```bash
# Run the chat flow with new question
pf flow test --flow . --inputs question="What's the capital of France?"

# Start a interactive chat session in the CLI
pf flow test --flow . --interactive

# Start a interactive chat session in CLI with verbose info
pf flow test --flow . --interactive --verbose
```

