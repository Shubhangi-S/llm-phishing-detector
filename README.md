# llm-phishing-detector

````markdown
# Malicious URL Detector (LLM + Heuristics)

Built by Shubhangi Singhal

This project detects malicious URLs in raw email or text content using basic heuristics and GPT-4 for classification. It’s written to be simple, testable, and cost-aware, without unnecessary complexity.

## What It Does

- Extracts all URLs from unstructured or structured email/text input
- Unshortens URLs and extracts basic risk signals (IP-based domains, keywords, encoded characters, etc.)
- Sends a structured prompt to GPT-4 to classify each URL as `malicious`, `safe`, or `unknown`
- Returns structured JSON output
- Includes logging and test cases for common input patterns

## Why I Built It This Way

- Heuristics are fast and free — used to filter noise before hitting GPT-4
- GPT-4 helps reason over ambiguous or edge-case URLs
- Testable, debuggable, and runs locally with no external dependencies beyond OpenAI + basic libraries

## Requirements

- Python 3.10+
- OpenAI Python SDK (`openai>=1.0.0`)
- `requests`, `tldextract`

Install dependencies:
```bash
pip install -r requirements.txt
````

## How to Run

1. Add your OpenAI key in `url_detector`:

   ```python
   client = OpenAI(api_key="your-openai-api-key")
   ```

2. Run on a sample email:

   ```bash
   python url_detector
   ```

3. Run unit tests:

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

* `url_detector.py` — Core pipeline, feature extraction, prompt building, GPT-4 classification, and tests
* `requirements.txt` — Required dependencies

## Notes

* Context size is capped at 1500 tokens for cost control
* The prompt to GPT-4 is concise and focused on extracted features
* Error handling and logging included for debugging
* Safe to run locally on CPU

## Things I’d Improve with More Time

* Add support for domain reputation and WHOIS APIs
* Improve feature set (e.g., TLD category, age of domain)
* Add caching and rate-limit protection for the LLM
* Support batch processing from inboxes or files
