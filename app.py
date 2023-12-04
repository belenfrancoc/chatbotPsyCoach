import openai, os, requests

openai.api_type = "azure"
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = "2023-08-01-preview"

# Azure OpenAI setup
openai.api_base = "https://open-ai-25.openai.azure.com/" # Add your endpoint here
openai.api_key = ("4e05e0cd314b4630ad351ad861139e7f") # Add your OpenAI API key here
deployment_id = "GPT4" # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://searchservice25.search.windows.net"; # Add your Azure AI Search endpoint here
search_key = ("K8uxsxGNNWDzYG8XrCG1zDBCkpuM10n3NNm3Y7AcwyAzSeBJ03Na"); # Add your Azure AI Search admin key here
search_index_name = "chatindex25"; # Add your Azure AI Search index name here

def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

setup_byod(deployment_id)


message_text = [{"role": "user", "content": "   Que es la salud mental?"}]

completion = openai.ChatCompletion.create(
    messages=message_text,
    deployment_id=deployment_id,
    dataSources=[  # camelCase is intentional, as this is the format the API expects
        {
            "type": "AzureCognitiveSearch",
            "parameters": {
                "endpoint": search_endpoint,
                "key": search_key,
                "indexName": search_index_name,
            }
        }
    ]
)
print(completion)