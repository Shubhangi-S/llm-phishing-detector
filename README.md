# Malicious URL Detector

**Built by Shubhangi Singhal**

This is a simple tool I built to check if URLs in emails or text messages might be dangerous (like phishing links). It uses a mix of basic rules (heuristics) and GPT-4 to make a decision for each link.

## What It Does

- Finds all URLs in raw text or email content  
- Expands shortened links to see where they really go  
- Looks at each link to find warning signs (like weird characters or IP addresses)  
- Sends a clean summary of each link to GPT-4 to label it as `malicious`, `safe`, or `unknown`  
- Returns easy-to-read JSON results  
- Includes unit tests

## Why I Built It This Way

- Basic rules are fast and don’t cost anything  
- GPT-4 is used only when needed — to make smarter decisions on tricky links  
- Everything runs locally with just a few libraries — no big setup required  
- Easy to test, update, and expand  

## Requirements

- Python 3.10+  
- `openai>=1.0.0`, `requests`, `tldextract`

To install everything:
```bash
pip install -r requirements.txt
```

## How to Run It

1. Add your OpenAI key in `url_detector.py` like this:
```python
client = OpenAI(api_key="your-api-key-here")
```

2. Run on a sample message:
```bash
python url_detector.py
```

3. Run tests:
```bash
python -m unittest url_detector
```

## Sample Output

```json
[
  {
    "url": "http://secure-login.phish.com",
    "verdict": "malicious",
    "confidence_score": 0.92
  },
  {
    "url": "https://www.example.com/safe",
    "verdict": "safe",
    "confidence_score": 0.98
  }
]
```

## Files

- `url_detector.py` – Main logic (extraction, prompt building, GPT-4 call, and tests)  
- `requirements.txt` – List of needed libraries  
- `url_detector.ipynb` – Jupyter notebook version for experimenting or demoing locally  
- `llm-url-detector-doc.md` – Full design and scope document explaining the approach and trade-offs  
- `LICENSE` – Standard open-source license file  
- `README.md` – This project readme  
- `.gitignore` – Standard Git ignore rules for Python + Jupyter projects  

## Notes

- Max LLM context is 1500 tokens (keeps cost low)  
- Prompts sent to GPT-4 are short and focused  
- Errors are handled clearly, and logs are printed to the console  
- Runs completely on your local machine — no special setup needed  

## Future Improvements (if I had more time)

- Add WHOIS checks or domain reputation lookups  
- Extract more features like domain age or top-level domain type  
- Add caching and rate limiting to better control OpenAI usage  
- Let it read from files or inboxes automatically  
