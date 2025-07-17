#!/usr/bin/env python
# coding: utf-8
# In[3]:

import re
import json
import requests
import logging
import unittest
from openai import OpenAI
from urllib.parse import urlparse

# === Logging Setup ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Config ===
LLM_MODEL = "gpt-4"
MAX_CONTEXT_TOKENS = 1500
client = OpenAI(api_key="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")  # Replace with your actual key

# === Utility Toolkit ===
class Tools:
    @staticmethod
    def unshorten_url(url):
        try:
            response = requests.head(url, allow_redirects=True, timeout=3)
            return response.url
        except requests.RequestException:
            logging.warning(f"Unshortening failed for {url}")
            return url

# === Heuristics + Feature Engineering ===
class URLFeatures:
    def extract_features(self, url):
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        domain_parts = hostname.split(".") if hostname else []
        domain = ".".join(domain_parts[-2:]) if len(domain_parts) >= 2 else hostname

        features = {
            "url": url,
            "domain": domain,
            "path_length": len(parsed.path),
            "query_length": len(parsed.query),
            "has_ip_address": bool(re.match(r"\\d+\\.\\d+\\.\\d+\\.\\d+", hostname)),
            "has_encoded_chars": "%" in url,
            "has_suspicious_keywords": any(k in url.lower() for k in ["login", "verify", "secure", "update"])
        }
        logging.debug(f"Extracted features for {url}: {features}")
        return features

# === Prompt Composer ===
class LLMPromptBuilder:
    def create_prompt(self, features):
        prompt = f"""
You are a cybersecurity assistant. Given these extracted features, classify the URL as 'malicious' or 'safe'.
Respond strictly in JSON format with the fields: 'url', 'verdict', and 'confidence_score' (0 to 1).

Features:
{json.dumps(features, indent=2)}
"""
        logging.debug("Prompt created for LLM:")
        logging.debug(prompt)
        return prompt

# === GPT Classifier ===
class LLMClassifier:
    def classify(self, prompt):
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=200
            )
            result = json.loads(response.choices[0].message.content)
            logging.info(f"Classification result: {result}")
            return result
        except Exception as e:
            logging.error(f"LLM classification failed: {e}")
            return {"verdict": "unknown", "confidence_score": 0.0, "error": str(e)}

# === Email Scanner Agent ===
class EmailAgent:
    def __init__(self):
        self.feature_engine = URLFeatures()
        self.llm = LLMClassifier()

    def extract_urls(self, text):
        urls = re.findall(r'(https?://[\w./\-]+)', text)
        logging.info(f"Extracted URLs: {urls}")
        return urls

    def process_email(self, email_text):
        urls = self.extract_urls(email_text)
        results = []
        for url in urls:
            resolved_url = Tools.unshorten_url(url)
            features = self.feature_engine.extract_features(resolved_url)
            prompt = LLMPromptBuilder().create_prompt(features)
            result = self.llm.classify(prompt)
            results.append(result)
        return results

# === Unit Tests ===
class TestEmailAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EmailAgent()

    def test_structured_email(self):
        email = "Click to verify at https://secure-login.fake-site.com and login."
        results = self.agent.process_email(email)
        self.assertTrue(len(results) > 0)
        self.assertIn("verdict", results[0])

    def test_unstructured_email(self):
        email = "Hey Bob, check this out: http://bit.ly/3xyzAbc"
        results = self.agent.process_email(email)
        self.assertTrue(len(results) > 0)
        self.assertIn("verdict", results[0])

# === Run Locally with Sample Email ===
if __name__ == "__main__":
    logging.info("Running Email Agent on sample email")
    sample_email = """
    Hey, we noticed suspicious activity. Please validate your login at http://secure-login.phish.com.
    For regular access, use https://www.example.com/safe.
    """
    agent = EmailAgent()
    results = agent.process_email(sample_email)
    print(json.dumps(results, indent=2))

    logging.info("Running unit tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
