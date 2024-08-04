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

# Add query to pass into messages for interactive conversation
query = input('Enter your desired query: ')

thread = client.beta.threads.create(
    messages=[{"role": "user", "content": query}],
    tool_resources={
        "file_search": {
            "vector_store_ids": [vector_id],
        }
    }
)

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistants_id,
    instructions="Please address the user as Security Advisor. The user has a inquiry on LLM Security specifically threats related to Generative AI in Cloud Computing.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
