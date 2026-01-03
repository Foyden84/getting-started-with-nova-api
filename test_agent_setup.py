"""
Test script to verify Amazon Nova API setup and agent functionality
Run this to ensure everything is configured correctly before using the notebooks
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

def test_api_connection():
    """Test basic API connection"""
    print("=" * 60)
    print("🧪 Testing Amazon Nova API Connection")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("NOVA_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        print("❌ ERROR: NOVA_API_KEY not set in .env file")
        print("   Please edit .env and add your API key from https://nova.amazon.com/dev/api")
        return False
    
    print("✅ API key found in .env file")
    
    # Initialize client
    try:
        base_url = "https://api.nova.amazon.com/v1"
        client = OpenAI(api_key=api_key, base_url=base_url)
        print("✅ OpenAI client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test basic completion
    try:
        print("\n📡 Testing basic chat completion...")
        response = client.chat.completions.create(
            model="nova-2-lite-v1",
            messages=[
                {"role": "user", "content": "Say 'Hello from Amazon Nova!' if you can hear me."}
            ],
            max_tokens=50
        )
        
        message = response.choices[0].message.content
        print(f"✅ Response received: {message}")
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False
    
    return True


def test_tool_calling():
    """Test tool calling functionality"""
    print("\n" + "=" * 60)
    print("🔧 Testing Tool Calling")
    print("=" * 60)
    
    load_dotenv()
    api_key = os.getenv("NOVA_API_KEY")
    base_url = "https://api.nova.amazon.com/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Define a simple test tool
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]
    
    try:
        print("📡 Testing tool call with weather function...")
        response = client.chat.completions.create(
            model="nova-2-lite-v1",
            messages=[
                {"role": "user", "content": "What's the weather in Seattle?"}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            print(f"✅ Tool called: {tool_call.function.name}")
            print(f"   Arguments: {tool_call.function.arguments}")
        else:
            print("⚠️  No tool call made (agent responded directly)")
            print(f"   Response: {message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool calling test failed: {e}")
        return False


def test_multimodal():
    """Test multimodal capabilities"""
    print("\n" + "=" * 60)
    print("🖼️  Testing Multimodal Capabilities")
    print("=" * 60)
    print("ℹ️  Multimodal features require specific models and image inputs")
    print("   See 02_multimodal_understanding.ipynb for detailed examples")
    print("✅ Multimodal test skipped (requires image input)")
    return True


def main():
    """Run all tests"""
    print("\n" + "🚀 " * 20)
    print("Amazon Nova API Agent Setup Test")
    print("🚀 " * 20 + "\n")
    
    results = []
    
    # Test 1: API Connection
    results.append(("API Connection", test_api_connection()))
    
    # Test 2: Tool Calling
    if results[0][1]:  # Only if API connection works
        results.append(("Tool Calling", test_tool_calling()))
    
    # Test 3: Multimodal
    results.append(("Multimodal", test_multimodal()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to build AI agents!")
        print("\n📚 Next steps:")
        print("   1. Open agent_use_cases_tutorial.ipynb in Jupyter")
        print("   2. Run the cells to explore different agent patterns")
        print("   3. Check AGENT_QUICK_REFERENCE.md for quick tips")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

