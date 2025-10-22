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

That's it! You're now ready to use the Python package and manage your environment variables securely.

# Working with this in Azure AI Foundry #

## Updates from March 2025 ##
- Evaluations Lab is shown in course this will evolve with Automation of Evaluations
- Added DeepSeek R1 using LangChain + Exa AI this is housed in /14-azure-ai-inference
- In-progress (Agents in Azure Foundry via SDK)

## Updates planned for Summer 2025 ##
- Distillation
- Response API Updates
- Automated Red Team Agent (Evaluation of Application using PyRiT)

This assumes you have deployed the Azure AI Foundry + Workspace (Project) in a supported region East US 2 (US) see reference.
https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/simulator-interaction-data

Once you've used environment variables for the items in the script the modification is located on lines 77-85
The amount of turns, results, and jailbreak can change use the guidance on the evaluation that you'd like to test with this service.
