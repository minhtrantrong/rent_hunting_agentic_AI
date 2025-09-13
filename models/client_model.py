from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import yaml
import os
from typing import Optional, Dict, Any

# Load environment variables once at module level
load_dotenv()

def _load_model_configs() -> Dict[str, Any]:
    """Load model configurations from config file."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config.get('models', {})
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing config file: {e}")

# Load configurations at module level
MODEL_CONFIGS = _load_model_configs()

def load_model_instance(
    model: str = "gemini", 
    temperature: Optional[float] = None,
    markdown: bool = True,
    instructions: Optional[str] = None,
) -> Agent:
    """
    Load and configure an AI agent with the specified model and instructions.

    Args:
        model: Model name (default: "gemini")
        temperature: Override default temperature
        markdown: Enable markdown formatting
        instructions: Custom instructions for the agent
        **kwargs: Additional agent configuration
    
    Returns:
        Configured Agent instance
        
    Raises:
        ValueError: If model is not supported
    """
    if model not in MODEL_CONFIGS:
        raise ValueError(f"Unsupported model: {model}. Available: {list(MODEL_CONFIGS.keys())}")
    
    config = MODEL_CONFIGS[model].copy()
    provider = config.pop('provider', 'google')
    
    # Override temperature if provided
    if temperature is not None:
        config["temperature"] = temperature
    
    # Create model instance based on provider
    if provider == "google":
        model_instance = Gemini(**config)
    else:
        raise ValueError(f"Provider not implemented: {provider}")
    
    return model_instance

