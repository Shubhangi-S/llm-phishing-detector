
# Design + Scope Document — LLM-Powered Malicious URL Detector

## Overview

This document explains how I designed and implemented a URL detector using GPT-4 to identify potentially malicious links in emails. I was inspired by the “phishing_pot” idea mentioned in the prompt, but since the original repo was unavailable, I implemented the solution independently.

The goal was to create a working proof of concept (POC) that shows how large language models (LLMs) can help with security tasks like phishing detection — without making things overly complex.

---

## Problem Scope

I needed to build a system that:

1. Finds potential phishing URLs in structured or unstructured emails.
2. Labels each link as malicious or safe.
3. Returns a clear JSON output with results.
4. Includes a confidence score if there’s uncertainty.
5. Stays within a 1500-token LLM limit.
6. Uses smart tools like WHOIS, link unshortening, or pattern checks when needed.

---

## Assumptions & Simplifications

- This is a local demo, not a production app.
- I didn't include memory, user sessions, or a database.
- WHOIS and link unshortening were kept simple or mocked.
- If the model fails, the output is marked "unknown."
- I tried to keep API calls and cost low.
- Focused on making the system flexible and easy to extend.

---

## Design Decisions & Technical Approach

- Wrote everything in Python using separate modules: extractor, prompt_builder, classifier.
- GPT-4 was used as the main decision-maker.
- Each call to GPT-4 is isolated with built-in error handling.
- I used regular expressions, tldextract, and simple checks to pull out link data.
- The logic follows a step-by-step pattern: extract → analyze → classify.
- The app runs from the command line for easy local testing.

---

## Trade-offs & Rationale

- **GPT-4** is accurate but costly and slower than smaller models.
- **Skipped traditional ML** — no training required, faster to build, easier to maintain.
- **Simplified tooling** — things like WHOIS and unshortening were basic. It’s enough for the demo but not production-grade.
- **No deployment setup** — I didn’t include servers, APIs, or databases.
- **Clear JSON format** — simple for anyone to read or extend later.
- **Fallbacks** — instead of guessing, the model says “unknown” when unsure.
- **No monitoring/retries** — this made things faster to prototype but not production-ready.

---

## Parsing Strategy

To find URLs:

- I used a regular expression to pull out anything that looked like a link.
- If the link was shortened (like bit.ly), I tried to get the real link behind it.
- I broke each URL into parts like domain, path, and query using standard Python tools.

```python
re.findall(r'(https?://[\w./\-]+)', text)
```

---

## Feature Extraction + Context Optimization

### Key Features I Used:

- Main domain (like example.com)
- Length of the URL path
- Length of query string
- Use of strange characters (like `%20`)
- Words that are often used in scams (like “verify” or “secure”)
- Whether the domain is just an IP address

### Why These?

They’re simple, take little space in the LLM prompt, and still give good signals. I kept the total input to under 300 tokens so I could stay far from the 1500-token limit.

---

## Prompt Construction (LLMPromptBuilder)

- The LLM was asked to behave like a security assistant.
- I gave it the features from each URL in structured JSON.
- I clearly told the model to respond with just two fields:
  - `verdict`: safe, malicious, or unknown
  - `confidence_score`: a number (optional)

---

## Classification Logic (LLMClassifier)

- The features were sent to GPT-4 using the OpenAI SDK.
- If GPT-4 gave a clean JSON answer, I used that.
- If something went wrong (timeout, formatting), I returned “unknown” and moved on.

---

## AI Track: Agentic Reasoning

### What My Agent Did:

1. **Extracted the link**
2. **Unshortened it**, if it was a tinyurl or bit.ly-style link
3. **(Mocked) WHOIS check**, just to include the idea
4. Ran simple rules to look for odd patterns

### What Happens If Something Fails?

If any of these steps fail, the app doesn’t crash. It just marks the output as unknown or uses the best info available.

---

## Traditional ML + LLM (Optional)

This project didn’t include traditional machine learning, but I thought about it.

Here’s what I could add later:

- A basic ML model (like logistic regression) to pre-filter links
- Only send confusing cases to GPT-4 to save cost
- This could help scale the system later on

---

## Security Track: Anti-Abuse System Design

### What Types of Dangerous Links I Considered

1. **Shortened Links**
   - These hide the real website behind a short code.
   - You don’t know where they go until you click.

2. **Fake-Looking Websites**
   - Look like real companies, but are fake.
   - Examples: `gooogle.com`, `paypa1.com`, `ɢoogle.com`

### How I Try to Catch These

- **Unshorten the link** to find the real destination.
- **Check the domain** — does it look almost like a real company?
- **Check DNS records** — real companies usually have proper email and DNS setup.

### How I Think Like an Attacker

I didn’t focus on surface features like logo or page title — those can be faked.

Instead, I looked at:

- Link structure
- Odd characters or very long paths
- Sneaky tricks like using numbers instead of letters

---

## Test Coverage

I added two main test cases:

1. An email with a suspicious link hidden inside
2. A casual message with a shortened URL

Both test end-to-end: extraction, analysis, and LLM verdict.

---

## Summary

This project shows how an LLM like GPT-4 can be used to detect phishing links in a clear and practical way.

GitHub Repo: [https://github.com/Shubhangi-S/llm-phishing-detector](https://github.com/Shubhangi-S/llm-phishing-detector)

Prepared by: **Shubhangi Singhal**  
July 2025
