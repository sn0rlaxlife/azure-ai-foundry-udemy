#### Prompt-flow demo ####
This is a adaption of the example provided here https://github.com/microsoft/promptflow/tree/main/examples/flows/chat/chat-with-wikipedia

### Prerequisites ###
Install the promptflow sdk and other dependencies in this folder.

```bash
pip install -r requirements.txt
```

### Example provided in the flow ###
Prompt template format of what the LLM tool chat api will interpret is shown below
```bash
# system:
You are a chatbot having a conversation with a human.

# user:
{{question}}
```
The {{question}} is pulled from the input we pass in the system is directed to consider the context as a conversation.

### Connecting to Promptflow ###
1. We have to establish our connection with Azure OpenAI API this is faciliated with the example file in the directory azure_openai.yml.example (you'd replace the .example) don't commit this is in the .gitignore so you don't check it into the repository.

```yaml
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/AzureOpenAIConnection.schema.json
name: open_ai_connection
type: azure_open_ai
api_key: <api_key> # do not commit this (.example) is to provide you a reference for creating this
api_base: <base_url> # provided by Azure OpenAI
api_type: <azure> # if using Azure OpenAI
```
2. Establish the connection
```bash
pf connection create --file azure_openai.yml
```
3. In the flow.dag.yaml you want to connect the open_ai_connection this can change the model depending on the existing deployment you are running.
```yaml
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
4. Execute the chat
```bash
# run chat flow with default question in flow.dag.yaml
pf flow test --flow .

# run chat flow with new question
pf flow test --flow . --inputs question="What's Generative AI?"

# start a interactive chat session in CLI
pf flow test --flow . --interactive

# start a interactive chat session in CLI with verbose info
pf flow test --flow . --interactive --verbose
```




