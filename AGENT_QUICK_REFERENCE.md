# AI Agent Quick Reference Guide

## 🎯 Agent Use Cases Overview

### 1. Customer Support Agent
**Purpose**: Handle customer inquiries, check orders, manage support tickets

**Key Tools**:
- `search_knowledge_base()` - Search FAQs and policies
- `check_order_status()` - Track orders
- `create_support_ticket()` - Escalate issues

**Best For**: Customer service automation, FAQ handling, order management

---

### 2. Research Assistant Agent
**Purpose**: Search information, summarize findings, conduct research

**Key Tools**:
- `web_search()` - Find information online
- `save_research_note()` - Store findings

**Best For**: Market research, competitive analysis, information gathering

---

### 3. Data Analysis Agent
**Purpose**: Analyze datasets, identify trends, generate insights

**Key Tools**:
- `calculate_statistics()` - Mean, median, std, etc.
- `analyze_trend()` - Trend detection

**Best For**: Business intelligence, sales analysis, performance monitoring

---

### 4. Task Automation Agent
**Purpose**: Automate workflows, schedule tasks, manage files

**Key Tools**:
- `send_email()` - Email notifications
- `schedule_task()` - Task scheduling
- `create_file()` - File management

**Best For**: Workflow automation, notifications, task management

---

### 5. Multi-Agent System
**Purpose**: Coordinate multiple specialized agents

**Components**:
- Router agent - Directs requests
- Specialist agents - Handle specific domains
- Aggregator - Combines results

**Best For**: Complex workflows requiring multiple capabilities

---

## 🛠️ Tool Definition Template

```python
{
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "Clear description of what the tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param_name": {
                    "type": "string",  # or "number", "boolean", "array", "object"
                    "description": "What this parameter does",
                    "enum": ["option1", "option2"]  # Optional: constrain values
                }
            },
            "required": ["param_name"]  # List required parameters
        }
    }
}
```

---

## 🚀 Agent Implementation Pattern

```python
def run_agent(user_message):
    # 1. Setup messages
    messages = [
        {"role": "system", "content": "Agent instructions..."},
        {"role": "user", "content": user_message}
    ]
    
    # 2. Initial API call
    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        tools=agent_tools,
        tool_choice="auto"
    )
    
    # 3. Handle tool calls
    if response.choices[0].message.tool_calls:
        messages.append(response.choices[0].message)
        
        for tool_call in response.choices[0].message.tool_calls:
            # Execute tool
            result = execute_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
            
            # Add result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
        
        # 4. Get final response
        final_response = client.chat.completions.create(
            model=model_id,
            messages=messages
        )
        return final_response.choices[0].message.content
    
    return response.choices[0].message.content
```

---

## 📊 Model Selection Guide

| Model | Use Case | Speed | Cost | Capabilities |
|-------|----------|-------|------|--------------|
| `nova-2-lite-v1` | Simple tasks, high volume | ⚡⚡⚡ | 💰 | Basic reasoning |
| `nova-2-pro-v1` | Complex reasoning | ⚡⚡ | 💰💰 | Advanced reasoning |
| `nova-2-micro-v1` | Ultra-fast, simple | ⚡⚡⚡⚡ | 💰 | Very basic |

---

## ✅ Best Practices Checklist

- [ ] Use descriptive tool names and descriptions
- [ ] Validate all inputs before processing
- [ ] Handle errors gracefully with clear messages
- [ ] Keep system prompts clear and focused
- [ ] Test with edge cases and unexpected inputs
- [ ] Monitor token usage and costs
- [ ] Implement logging for debugging
- [ ] Use environment variables for secrets
- [ ] Cache frequently used results
- [ ] Implement rate limiting for production

---

## 🔧 Common Patterns

### Pattern 1: Sequential Tool Calls
Agent calls multiple tools in sequence to complete a task.

### Pattern 2: Conditional Logic
Agent decides which tool to use based on context.

### Pattern 3: Iterative Refinement
Agent calls tools, analyzes results, and may call again.

### Pattern 4: Parallel Processing
Multiple agents work on different aspects simultaneously.

---

## 📚 Additional Resources

- **Tutorial Notebook**: `agent_use_cases_tutorial.ipynb`
- **Basic Examples**: `00_getting_started.ipynb` through `04_nova_api_strands_sdk.ipynb`
- **Advanced Examples**: `langchain/`, `strands/`, `nova_agents/`
- **Documentation**: https://nova.amazon.com/dev/documentation

