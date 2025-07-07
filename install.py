#!/usr/bin/env python3
"""
Installation script for Smriti Memory Library
This script helps set up the smriti memory library with proper dependencies.
"""

import os
import sys
import subprocess
import platform


def print_banner():
    """Print installation banner."""
    print("🚀 Smriti Memory Library Installation")
    print("=" * 50)
    print("An intelligent memory layer for AI applications")
    print("=" * 50)


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("Please use Python 3.8 or higher.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install the package in development mode
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("✅ Package installed successfully")
        
        # Install development dependencies if requested
        install_dev = input("\n🤔 Install development dependencies? (y/n): ").lower().strip()
        if install_dev in ['y', 'yes']:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
            print("✅ Development dependencies installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_api_keys():
    """Check if required API keys are set."""
    print("\n🔑 Checking API keys...")
    
    required_keys = {
        "PINECONE_API_KEY": "Pinecone vector database",
        "GROQ_API_KEY": "Groq LLM service",
        "GEMINI_KEY": "Google Gemini embeddings"
    }
    
    missing_keys = []
    for key, description in required_keys.items():
        if os.getenv(key):
            print(f"✅ {key} is set ({description})")
        else:
            print(f"⚠️  {key} is not set ({description})")
            missing_keys.append(key)
    
    if missing_keys:
        print(f"\n⚠️  Missing API keys: {', '.join(missing_keys)}")
        print("You'll need to set these environment variables:")
        
        for key in missing_keys:
            print(f"  export {key}='your-api-key'")
        
        print("\nOr create a .env file with:")
        for key in missing_keys:
            print(f"  {key}=your-api-key")
        
        return False
    
    print("✅ All API keys are configured")
    return True


def create_env_file():
    """Create a .env file template."""
    print("\n📝 Creating .env file template...")
    
    env_template = """# Smriti Memory Library Configuration
# Replace these with your actual API keys

# Pinecone vector database
PINECONE_API_KEY=your-pinecone-api-key

# Groq LLM service
GROQ_API_KEY=your-groq-api-key

# Google Gemini embeddings
GEMINI_KEY=your-gemini-api-key

# Optional: Custom configuration
# LLM_MODEL=llama-3.1-8b-instant
# LLM_TEMPERATURE=0.3
# DEFAULT_NAMESPACE=user_understanding
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_template)
        print("✅ Created .env file template")
        print("📝 Edit .env file with your actual API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def test_installation():
    """Test if the installation works."""
    print("\n🧪 Testing installation...")
    
    try:
        # Try to import the library
        import smriti
        print("✅ Library imports successfully")
        
        # Try to create a memory manager
        from smriti import MemoryManager
        memory_manager = MemoryManager()
        print("✅ Memory manager can be created")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def show_next_steps():
    """Show next steps for the user."""
    print("\n🎉 Installation completed!")
    print("\n📚 Next steps:")
    print("1. Set up your API keys (see .env file)")
    print("2. Run the test script: python test_smriti.py")
    print("3. Try the examples: python example_usage.py")
    print("4. Use the CLI: smriti --help")
    print("5. Read the README.md for detailed documentation")
    
    print("\n💡 Quick start:")
    print("```python")
    print("from smriti import MemoryManager")
    print("memory_manager = MemoryManager()")
    print("result = memory_manager.add_memory('user123', [{'user': 'I like pizza'}])")
    print("```")


def main():
    """Main installation process."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Check API keys
    api_keys_ok = check_api_keys()
    
    # Create .env file if API keys are missing
    if not api_keys_ok:
        create_env_file()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed. Please check the error messages above.")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main() 