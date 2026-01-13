# Define the models to use in the agent

from os_computer_use import providers
import os

# Grounding Model
try:
    # Try OSAtlas first
    grounding_model = providers.OSAtlasProvider()
except Exception as e:
    print(f"Warning: Failed to initialize OSAtlasProvider: {e}")
    try:
        # Fallback to ShowUI
        grounding_model = providers.ShowUIProvider()
    except Exception as e:
        print(f"Warning: Failed to initialize ShowUIProvider: {e}")
        grounding_model = providers.DummyGroundingProvider("Grounding models failed to initialize")

# Vision Model
if os.getenv("OPENROUTER_API_KEY"):
    try:
        vision_model = providers.OpenRouterProvider("qwen-2.5-vl")
    except Exception as e:
        print(f"Warning: Failed to initialize OpenRouterProvider: {e}")
        vision_model = providers.DummyLLMProvider("OpenRouterProvider failed")
else:
    print("Warning: Missing OPENROUTER_API_KEY. Using DummyLLMProvider for vision_model.")
    vision_model = providers.DummyLLMProvider("Missing OPENROUTER_API_KEY")

# Action Model
if os.getenv("GROQ_API_KEY"):
    try:
        action_model = providers.GroqProvider("llama-3.3")
    except Exception as e:
        print(f"Warning: Failed to initialize GroqProvider: {e}")
        action_model = providers.DummyLLMProvider("GroqProvider failed")
else:
    print("Warning: Missing GROQ_API_KEY. Using DummyLLMProvider for action_model.")
    action_model = providers.DummyLLMProvider("Missing GROQ_API_KEY")
