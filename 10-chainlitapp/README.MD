# 10-Chainlit Application

## Description
This application uses Chainlit to perform various tasks. This README will guide you through setting up the virtual environment and configuring the environment variables.

## Prerequisites
- Python 3.x
- `pip` (Python package installer)

## Setup

### 1. Clone the Repository
```sh
git clone https://github.com/sn0rlaxlife/azure-ai-studio-udemy.git
cd 10-chainlitapp
```

### 2. Setup the Virtual Environment
Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
Install the required Python packages:
```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of the project and add the necessary environment variables:

This lab does require a API Key from EXA.AI -> retrieve this via https://exa.ai/
```sh
cp .env.example .env
# Edit .env to include your specific environment variables
```

### 5. Running the applicaiton locally
This code uses chainlit that provides a UI frontend you can run this as the following
```sh
chainlit run app.py -w
```

This will have a localhost url generated go to the localhost and query your request to interact with chainlit applicaiton
