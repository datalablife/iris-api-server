# 🔐 Secure API Testing Scripts

## ⚠️ Security Notice

**NEVER hardcode API keys in scripts!** All API keys must be provided via environment variables.

## 🛡️ Secure Usage

### 1. Set Environment Variable
```bash
# Set your API key (replace with your actual key)
export GOOGLE_API_KEY="your_actual_api_key_here"
```

### 2. Verify Environment Variable
```bash
# Check if API key is set (shows only first 10 characters)
echo "API Key: ${GOOGLE_API_KEY:0:10}..."
```

### 3. Run Tests
```bash
# Run secure test scripts
./test_secure_gemini.sh
```

## 📝 Script Template

Here's the secure template for all API test scripts:

```bash
#!/bin/bash

# Secure API Test Script Template
echo "Testing Gemini API..."

# SECURITY CHECK: Verify API key is set via environment variable
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ Error: GOOGLE_API_KEY environment variable is not set"
    echo "Please set your API key: export GOOGLE_API_KEY='your_api_key_here'"
    exit 1
fi

# Use environment variable (NEVER hardcode keys)
API_KEY="$GOOGLE_API_KEY"

# Show masked key for verification
echo "🔑 Using API key: ${API_KEY:0:10}..."

# Your API test code here...
```

## 🚨 Security Incident

**Previous versions of scripts in this directory contained hardcoded API keys that were exposed in the public repository. These files have been removed and the exposed key should be revoked immediately.**

See `SECURITY_ALERT.md` for full details.

## ✅ Best Practices

1. **Environment Variables Only**: Never hardcode credentials
2. **Masked Logging**: Only show first few characters of keys in logs
3. **Error Handling**: Always check if environment variables are set
4. **Documentation**: Clearly document required environment variables
5. **Version Control**: Never commit files with actual API keys

## 🔍 Verification

To ensure no API keys are hardcoded:
```bash
# Search for potential API key patterns
grep -r "AIzaSy" . --exclude-dir=.git
grep -r "sk-" . --exclude-dir=.git
grep -r "api_key.*=" . --exclude-dir=.git
```

## 📚 Resources

- [Google API Key Security](https://cloud.google.com/docs/authentication/api-keys)
- [Environment Variable Best Practices](https://12factor.net/config)
- [Git Secrets Prevention](https://github.com/awslabs/git-secrets)
