## Azure Foundry AI Agent Service ##
Demo annotated in the agent.py is the representation of the Lab 15.

## Getting started ##
- Requirements
- GPT-4o (Mini is used in this demo) you can use your preferred model that is supported
- Agents defined via UI if its easier this assumes you have three agents defined (Finance, Writer, Editor) these can be created in the portal as shown
- Bing Search (Resource deployed) this includes the search functionality
- Environment variables follow .env.example

Step 1 - set up virtual environment
```bash
git clone https://github.com/sn0rlaxlife/azure-ai-foundry-udemy.git
cd 15-azure-agents
python -m venv venv
source /venv/bin/activate (macOS) for Windows /bin/Activate.ps1
```

Step 2 - Make a copy of .env.example as the following ensure you have a gitignore this is included to ensure no commits
```bash
touch .env
```

Step 3 - Install requirements
```bash
pip install -r requirements.txt
```

Step 4 - Login to azure to authenticate token from project
```bash
az login --use-device-code
```

Step 5 - Run the agent.py once you have .env populated with the following variables
```bash
AZURE_AI_AGENT_PROJECT_CONNECTION_STRING='<Connection-string>'
AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME='<deployment-name>'
FINANCE_AGENT_ID='<->'
EDITOR_AGENT_ID='<->'
WRITER_AGENT_ID='<-writing-id>'
BING_SEARCH_SUBSCRIPTION_KEY='<bing-key>'
BING_SEARCH_URL="<bing-url>"
```

Then run
```bash
python3 agent.py
```
