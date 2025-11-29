# Nova Agent Examples

This folder demonstrates how to use the Nova API to use Amazon Nova models to build agentic applications. These are simple examples meant to spark ideas and serve as a starting point for development.

## Table of Contents
* [Strands Agents and Nova](#strands-and-nova)
* [Image Analysis and Computer Use](#image-analysis-and-computer-use)
* [Knowledge Grounding and Computer Use](#knowledge-grounding-and-computer-use)

## Strands Agents and Nova

[`planet_story_strands.py`](planet_story_strands.py)

A Strands Agents implementation that coordinates UI automation with Nova Act and Nova Lite for story generation using the Strands framework.

**Features:**
- Uses Strands Agents framework for orchestration
- Custom tool for planet data extraction with Nova Act
- Uses Strands HTTP tool to call Nova 2 Lite API
- Demonstrates agent-based architecture with tool composition

**Usage:**
```bash
# Install dependencies (includes strands-agents)
pip install -r requirements.txt

# Set up your Nova API key in .env file
echo "NOVA_API_KEY=your_api_key_here" > .env

# Run the Strands agent
python planet_story_strands.py
```

## Image Analysis and Computer Use 

[`visual_planet_explorer.py`](visual_planet_explorer.py)

Uses Nova Act to navigate the web browser to find the planet profile and analyzes its "vibe" using Nova's Image Analysis capabilities based on visual presentation elements like colors, design, and layout.

**Features:**
- Uses Nova Act to navigate and analyze planet visual presentation
- Extracts detailed visual descriptions (colors, layout, design aesthetic)
- Uses Nova 2 Lite to interpret the overall vibe and atmosphere
- Demonstrates combining navigation with visual analysis

**Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up your Nova API key in .env file
echo "NOVA_API_KEY=your_api_key_here" > .env

# Run the visual explorer
python visual_planet_explorer.py
```

## Knowledge Grounding and Computer Use 

[`grounded_planet_research.py`](grounded_planet_research.py)

Combines Nova Grounding to research real exoplanets, creating a comparison between science fiction and reality with Nova Act's UI automation for exploring fictional planets.

**Features:**
- Uses Nova Grounding to research real exoplanets with similar characteristics
- Uses Nova Act to extract information about fictional planets from the gym
- Use Nova Lite to compare fictional planets to actual astronomical discoveries
- Generates insights about sci-fi vs reality
- Demonstrates combining web navigation with grounded real-world research

**Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up your Nova API key in .env file
echo "NOVA_API_KEY=your_api_key_here" > .env

# Run the grounded research agent
python grounded_planet_research.py
```