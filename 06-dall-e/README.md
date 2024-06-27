### Generate Images with DALL-E 3 Model ###

Requirements
- Azure OpenAI Service Deployed
- Dall-e 3 Model

## Setup ##
This uses environment variables however, if you'd want to retrieve these in a production scenario you'd likely use a KMS system such as Azure Key Vault.
1. Clone the repository
```bash
git clone https://github.com/sn0rlaxlife/azure-ai-studio.git
```
2. Navigate to this directory
```bash
cd 06-dall-e
```
3. Create a virtual environment (Recommended)
```bash
python -m venv venv
```
4. Activate the virtual env
   * For windows
     ```bash
     venv\Scripts\activate
     ```
   * For MacOS/Linux
   ```bash
   source venv/bin/activate
   ```
5. Install the project requirements
```bash
pip install -r requirements.txt
```
6. Set environment variables
   ```bash
   setx AZURE_OPENAI_ENDPOINT=<endpoint>
   setx DALLE3_DEPLOYMENT=<deployment-name>
   setx AZURE_OPENAI_API_KEY=<api-key>
   ```
### Usage ###
1. Run the main.py
   ```bash
   python main.py
   ```
   This will allow you to input a prompt the try/exception is a check to ensure a prompt is passed through.
2. A URL will be generated once the DALLE-3 script is complete
   


