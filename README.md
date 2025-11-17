# Nova API Examples

This repository contains Python scripts and Jupyter notebooks demonstrating how to interact with Amazon Nova AI models using their API.

## Prerequisites

- Python 3.x
- Jupyter Notebook (for running .ipynb files)
- Nova API Key from Amazon

## Setup

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your API key:
   - Open `nova_key.py`
   - Replace `<YOUR_NOVA_API_KEY_GOES_HERE` with your actual Nova API key

## Files Overview

### Configuration Files

**nova_key.py**
- Stores your Nova API key
- Required by all other scripts and notebooks
- Must be configured before running any examples

**requirements.txt**
- Lists Python dependencies (currently: `openai`)
- Install with: `pip install -r requirements.txt`

### Python Scripts

**list_models.py**
- Lists all Nova models available for your API key
- Displays model display names and IDs
- Execute with:
```bash
python list_models.py
```

### Jupyter Notebooks

**single_turn.ipynb**
- Demonstrates single-turn interactions with Nova models
- Examples include:
  - Simple greeting interaction
  - Question answering about GenAI topics
- Uses the OpenAI SDK with Nova API endpoint
- Execute: Open in Jupyter and run cells sequentially

**multi_turn.ipynb**
- Shows multi-turn conversation capabilities
- Example: Recipe generation with follow-up modifications
- Demonstrates conversation history management
- Execute: Open in Jupyter and run cells sequentially

**nova_tools.ipynb**
- Comprehensive guide to Nova's tool calling capabilities
- Covers:
  - Auto tool selection (calculator, search, code generation)
  - Custom tool definition and usage
  - Tool chaining (combining auto and custom tools)
- Examples include:
  - Mathematical calculations
  - Web search queries
  - Code generation
  - Unit conversion with custom tools
- Execute: Open in Jupyter and run cells sequentially

**nova_api_strands_sdk.ipynb**
- Demonstrates using Strands Agent's HTTP tool to call Nova APIs
- Alternative approach to making API calls
- Requires additional dependency: `strands-agents-tools`
- Execute: Open in Jupyter and run cells sequentially

## Running the Examples

### For Python Scripts:
```bash
python list_models.py
```

### For Jupyter Notebooks:
```bash
jupyter notebook
```
Then open the desired notebook and run cells in order.

## Common Workflow

1. Set up your API key in `nova_key.py`
2. Install dependencies: `pip install -r requirements.txt`
3. Check available models: `python list_models.py`
4. Explore notebooks starting with `single_turn.ipynb`
5. Progress to more advanced examples like `nova_tools.ipynb`

## Model Configuration

The notebooks use `nova-lite-v2` by default. You can change the model by modifying the `NOVA_MODEL_ID` variable in each notebook.

## API Endpoint

All examples connect to: `https://api.nova.amazon.com/v1`
