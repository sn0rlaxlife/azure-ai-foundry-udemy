### Prompt flow using Research ###

This is actively in development but the sole purpose is to demonstrate the use of prompt flow building your own flow

## Requirements ###
* Azure OpenAI (GPT deployed) can be serverless if you use a separate model will have another folder covering mistral/llama
* Python installed
* Promptflow VS Code Extension

### Installation ###
1. Clone the repository
```bash
git clone https://github.comc/sn0rlaxlife/azure-ai-studio-udemy.git
cd /07-research-flow
```

2. Create a virtual environment
```bash
python -m venv flow
```
3. Activate the virtual environment
For windows
```bash
.\flow\Scripts\activate
```
For MacOS and Linux
```bash
source flow/bin/activate
```
4. Install related dependencies
```bash
python3 install -r requirements.txt
```
5. Create a connection to promptflow - this bridges the API connection locally
```bash
pf connection create --file <openai.yaml>
```
6. Edit the flow.dag.yaml to replace with the deployment name shown below
```bash
  inputs:
    # This is to easily switch between openai and azure openai.
    # deployment_name is required by azure openai, model is required by openai.
    deployment_name: gpt-35-turbo # the deployment name that you are consuming
    model: gpt-3.5-turbo #if you are using GPT-4o change this
    temperature: '0.8'
    question: ${inputs.question}
    chat_history: ${inputs.chat_history}
    contexts: ${process_search_result.output}
  connection: open_ai_connection
  api: chat
```

7. Execute the chat
```bash
   # run chat flow with new question
pf flow test --flow . --inputs question="What's Generative AI?"

# start a interactive chat session in CLI
pf flow test --flow . --interactive

# start a interactive chat session in CLI with verbose info
pf flow test --flow . --interactive --verbose
```
   
 
