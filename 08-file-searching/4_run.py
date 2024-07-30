import os
from typing_extensions import override
from openai import AssistantEventHandler, AzureOpenAI

# Vector ID from the vector store - vector.py
vector_id = os.getenv("VECTOR_STORE_ID")

# Assistants ID from our previous assistant creation
assistants_id= os.getenv("ASSISTANT_ID")

# Initialize the client call
client = AzureOpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )
 
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

thread = client.beta.threads.create(
    messages=[ {"role": "user", "content": "What are the top threats to cloud computing?"} ],
    tool_resources={
        "file_search": {
            "vector_store_ids": [vector_id],
        }
    }
)
