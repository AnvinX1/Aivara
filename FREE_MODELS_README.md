# Free Models Configuration

This project is configured to use **free models** from OpenRouter by default to avoid API costs.

## Current Configuration

### LLM Models (Chat/Completions)
- **Default**: `meta-llama/Llama-3.2-3B-Instruct-free`
- **Alternative Free Options**:
  - `meta-llama/Llama-3.1-8B-Instruct-free` (larger, slower)
  - `meta-llama/Llama-3.1-70B-Instruct-free` (very large, slower)
  - `mistralai/mistral-7b-instruct:free`

### Embedding Models
- **Default**: Local SentenceTransformer model (`sentence-transformers/all-MiniLM-L6-v2`)
- **Note**: Free embedding models on OpenRouter are limited, so we use the local fallback by default
- If you want to use OpenRouter embeddings, set `OPENROUTER_EMBED_MODEL` environment variable

## How to Change Models

### Using Environment Variables

**Windows PowerShell:**
```powershell
$env:OPENROUTER_API_KEY="your-api-key"
$env:OPENROUTER_MODEL="meta-llama/Llama-3.2-3B-Instruct-free"
# Or use Mistral:
$env:OPENROUTER_MODEL="mistralai/mistral-7b-instruct:free"
```

**Linux/macOS:**
```bash
export OPENROUTER_API_KEY="your-api-key"
export OPENROUTER_MODEL="meta-llama/Llama-3.2-3B-Instruct-free"
# Or use Mistral:
export OPENROUTER_MODEL="mistralai/mistral-7b-instruct:free"
```

### Available Free Models on OpenRouter

**Llama Models:**
- `meta-llama/Llama-3.2-3B-Instruct-free` (Recommended - fast and good quality)
- `meta-llama/Llama-3.1-8B-Instruct-free` (Better quality, slower)
- `meta-llama/Llama-3.1-70B-Instruct-free` (Best quality, slowest)

**Mistral Models:**
- `mistralai/mistral-7b-instruct:free`

**Note**: Model availability may change. Check [OpenRouter Models](https://openrouter.ai/models) for current free models.

## Embedding Models

The system uses a **local SentenceTransformer model** by default, which is completely free and doesn't require an API key. This model (`sentence-transformers/all-MiniLM-L6-v2`) provides good quality embeddings for RAG.

If you want to use OpenRouter embeddings instead:
```bash
export OPENROUTER_EMBED_MODEL="your-preferred-embedding-model"
```

However, free embedding models on OpenRouter are limited, so the local model is recommended.

## Configuration Files

The default models are set in:
- `config.py`: Main configuration
- `services/ai_engine.py`: LLM model default
- `app/services/embeddings_service.py`: Embedding model handling

## Cost Information

All configured models are **free**:
- ✅ Llama free models: No cost
- ✅ Mistral free models: No cost
- ✅ Local SentenceTransformer: No API cost
- ❌ OpenAI models (GPT-4, text-embedding-3-small): Paid

The system is designed to work entirely with free models to keep costs at zero.

