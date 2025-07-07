# Smriti Memory - Setup Guide

This guide will walk you through setting up Smriti Memory with all required API keys and configurations.

## 📋 What You Need

Smriti Memory requires API keys from three external services:

1. **Pinecone** - Vector database for storing and searching memories
2. **Groq** - LLM service for memory decisions and chat responses  
3. **Gemini** - Additional LLM capabilities

## 🔑 Getting Your API Keys

### 1. Pinecone API Key

**What it's for:** Storing and searching vector embeddings of your memories

**How to get it:**
1. Go to [pinecone.io](https://www.pinecone.io/)
2. Click "Get Started" and create a free account
3. Create a new project
4. Go to "API Keys" in your project dashboard
5. Copy your API key

**Free tier includes:**
- 1 project
- 1 index
- 100,000 operations per month
- Perfect for testing and small applications

### 2. Groq API Key

**What it's for:** LLM operations like deciding what to remember and generating chat responses

**How to get it:**
1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to "API Keys" in the console
4. Create a new API key
5. Copy the key

**Free tier includes:**
- 100 requests per minute
- Access to Llama 3.1 8B model
- No credit card required

### 3. Gemini API Key

**What it's for:** Additional LLM capabilities and fallback options

**How to get it:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

**Free tier includes:**
- 15 requests per minute
- Access to Gemini models
- No credit card required

## ⚙️ Configuration Options

### Option 1: Environment Variables (Recommended)

Create a `.env` file in your project root:

```bash
# .env
PINECONE_API_KEY=your-pinecone-api-key-here
GROQ_API_KEY=your-groq-api-key-here
GEMINI_KEY=your-gemini-api-key-here
```

Or set them in your shell:

```bash
export PINECONE_API_KEY="your-pinecone-api-key"
export GROQ_API_KEY="your-groq-api-key"
export GEMINI_KEY="your-gemini-api-key"
```

### Option 2: Direct Configuration

```python
from smriti import MemoryConfig, MemoryManager

config = MemoryConfig(
    pinecone_api_key="your-pinecone-key",
    groq_api_key="your-groq-key",
    gemini_api_key="your-gemini-key"
)

memory_manager = MemoryManager(config)
```

## 🚀 Quick Test

After setting up your API keys, test your installation:

```python
from smriti import MemoryManager

# This will use environment variables automatically
memory_manager = MemoryManager()

# Test adding a memory
chat_thread = [{"user": "I like pizza"}]
result = memory_manager.add_memory("test-user", chat_thread)
print("Memory added:", result["success"])

# Test searching
search_result = memory_manager.search_memories("test-user", "pizza")
print("Search results:", len(search_result["results"]))
```

## 🔧 Troubleshooting

### "Missing required configuration" Error

This means one or more API keys are missing. Check:

1. Environment variables are set correctly
2. No typos in the variable names
3. Keys are not empty or None

### Pinecone Connection Issues

1. Verify your Pinecone API key is correct
2. Check if your Pinecone project is active
3. Ensure you're using the correct environment (usually "us-east-1")

### Groq/Gemini API Errors

1. Verify API keys are correct
2. Check if you've exceeded free tier limits
3. Ensure your account is active

## 💰 Cost Considerations

**Free Tier Limits:**
- **Pinecone:** 100K operations/month
- **Groq:** 100 requests/minute
- **Gemini:** 15 requests/minute

**For Production:**
- Pinecone: Pay-as-you-go pricing
- Groq: Pay-per-request model
- Gemini: Pay-per-request model

## 🔒 Security Best Practices

1. **Never commit API keys to version control**
2. Use environment variables or secure secret management
3. Rotate keys regularly
4. Use the minimum required permissions
5. Monitor usage to avoid unexpected charges

## 📞 Support

If you encounter issues:

1. Check the [main README](../README.md) for detailed documentation
2. Review the [example usage](../example_usage.py) file
3. Run the test suite to verify your setup
4. Check the logs for detailed error messages

---

**Ready to start?** Head back to the [main README](../README.md) for usage examples and API documentation! 