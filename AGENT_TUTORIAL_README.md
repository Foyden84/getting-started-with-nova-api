# AI Agent Development Tutorial

## 🎯 What You'll Learn

This tutorial walks you through building **5 different types of AI agents** using Amazon Nova API:

1. **Customer Support Agent** - Automated customer service
2. **Research Assistant Agent** - Information gathering and analysis
3. **Data Analysis Agent** - Statistical analysis and insights
4. **Task Automation Agent** - Workflow automation
5. **Multi-Agent System** - Coordinating multiple specialized agents

## 📁 Files in This Tutorial

- **`agent_use_cases_tutorial.ipynb`** - Main tutorial notebook with all 5 use cases
- **`AGENT_QUICK_REFERENCE.md`** - Quick reference guide for agent patterns
- **`test_agent_setup.py`** - Test script to verify your setup
- **`AGENT_TUTORIAL_README.md`** - This file

## 🚀 Getting Started

### Step 1: Verify Setup
Run the test script to ensure everything is configured:

```bash
.\.venv\Scripts\python.exe test_agent_setup.py
```

You should see all tests pass ✅

### Step 2: Launch Jupyter
Start Jupyter Notebook:

```bash
.\.venv\Scripts\activate
jupyter notebook
```

### Step 3: Open the Tutorial
In Jupyter, open `agent_use_cases_tutorial.ipynb`

### Step 4: Run the Cells
Execute cells sequentially to learn each agent pattern

## 📚 Tutorial Structure

### Part 1: Setup (Cells 1-2)
- Import libraries
- Configure Nova API client
- Test connection

### Part 2: Customer Support Agent (Cells 3-6)
- Define support tools (knowledge base, order tracking, tickets)
- Implement tool functions
- Create agent with tool calling
- Test with customer queries

### Part 3: Research Assistant (Cells 7-9)
- Define research tools (web search, note saving)
- Build research agent
- Test with research queries

### Part 4: Data Analysis Agent (Cells 10-12)
- Define analysis tools (statistics, trends)
- Create data analyst agent
- Test with sample datasets

### Part 5: Task Automation Agent (Cells 13-15)
- Define automation tools (email, scheduling, files)
- Build automation agent
- Test with workflow tasks

### Part 6: Multi-Agent System (Cells 16-19)
- Create router agent
- Coordinate multiple specialists
- Test with various query types

### Part 7: Bonus Content (Cells 20-22)
- Strands SDK introduction
- Best practices
- Next steps and resources

## 🎓 Key Concepts

### Tool Calling
Agents use tools to interact with external systems:
```python
tools = [{
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "What it does",
        "parameters": {...}
    }
}]
```

### Agent Loop
1. User sends message
2. Agent decides if tools are needed
3. Agent calls tools
4. Agent synthesizes results
5. Agent responds to user

### System Prompts
Define agent behavior and personality:
```python
{
    "role": "system",
    "content": "You are a helpful assistant that..."
}
```

## 💡 Use Case Examples

### Customer Support
```python
run_customer_support_agent("What's your return policy?")
# Agent searches knowledge base and provides answer
```

### Research
```python
run_research_assistant("Find information about AI agents")
# Agent searches web and summarizes findings
```

### Data Analysis
```python
run_data_analyst("Analyze sales trends", data=[100, 120, 135, ...])
# Agent calculates statistics and identifies trends
```

### Automation
```python
run_automation_agent("Send report to team@company.com")
# Agent sends email and confirms delivery
```

### Multi-Agent
```python
mas.execute("Check order ORD-123")
# System routes to customer support agent automatically
```

## 🛠️ Customization Tips

### Add Your Own Tools
1. Define tool schema
2. Implement tool function
3. Add to agent's tool list
4. Update tool dispatcher

### Modify Agent Behavior
- Edit system prompts
- Adjust temperature (0 = deterministic, 1 = creative)
- Change model (lite vs pro)
- Add conversation memory

### Combine Agents
- Create specialized agents
- Build router logic
- Implement handoffs
- Aggregate results

## 📊 Performance Tips

- Use `nova-2-lite-v1` for simple tasks (faster, cheaper)
- Use `nova-2-pro-v1` for complex reasoning
- Cache frequently used results
- Batch similar requests
- Monitor token usage

## 🔒 Security Best Practices

- ✅ Validate all inputs
- ✅ Use environment variables for secrets
- ✅ Implement rate limiting
- ✅ Log all agent actions
- ✅ Get user consent for sensitive operations
- ❌ Never expose API keys in code
- ❌ Don't trust user input blindly

## 🐛 Troubleshooting

### "API key not found"
- Check `.env` file exists
- Verify `NOVA_API_KEY` is set
- Ensure no extra spaces

### "Tool not called"
- Check tool description is clear
- Verify parameters are correct
- Try more explicit user prompt

### "Rate limit exceeded"
- Wait and retry
- Implement exponential backoff
- Consider upgrading limits

## 📖 Additional Resources

### Official Documentation
- [Amazon Nova Docs](https://nova.amazon.com/dev/documentation)
- [API Reference](https://nova.amazon.com/dev/api)

### Example Notebooks
- `00_getting_started.ipynb` - Basics
- `01_multi_turn_interactions.ipynb` - Conversations
- `02_multimodal_understanding.ipynb` - Images/Video
- `03_tool_use_with_nova.ipynb` - Tool calling
- `04_nova_api_strands_sdk.ipynb` - Strands SDK

### Advanced Examples
- `langchain/` - LangChain patterns
- `strands/` - Strands SDK examples
- `nova_agents/` - Computer use agents

## 🤝 Contributing

Have ideas for new agent use cases? Create your own and share!

## 📝 License

MIT-0 License - See LICENSE file

---

**Happy Agent Building! 🤖✨**

