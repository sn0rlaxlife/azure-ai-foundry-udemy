import os
from openai import AzureOpenAI

# Steps for this as follows step 1 use the vector.py to create the vector store for our file searcher


client = AzureOpenAI(
    api_key= os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )


# Create a vector store called "security" with the following vectors
vector_store = client.beta.vector_stores.create(name="security")

#Ready the files we are referencing
file_paths = ["pdf/NIST.AI.100-1.pdf", "pdf/TopThreatstoCloudComputingPandemicEleven060622.pdf"]
file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them into our vector we've created,
# and then poll the status of the upload
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
   vector_store_id=vector_store.id, files=file_streams
)

# print the statues and file counts of the batch
print(file_batch.status)
print(file_batch.file_counts)
# This is needed for the assistant to have a reference to search from as a ID.
print(vector_store.id)
