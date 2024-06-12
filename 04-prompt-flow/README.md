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
