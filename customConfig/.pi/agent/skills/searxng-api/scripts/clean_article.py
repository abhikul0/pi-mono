#!/usr/bin/env python3
"""
Simple command‑line tool that fetches a URL, extracts the main article text and title, and prints a clean, readable version.

Usage:
    python clean_article.py <url>

The script performs the following steps:
1. Fetches the page using `requests`.
2. Parses the HTML with `beautifulsoup4`.
3. Uses `readability-lxml` to identify the main content block.
4. Removes script/style tags and any elements that look like ads or navigation.
5. Prints the title and cleaned article text.

Dependencies:
    pip install requests beautifulsoup4 readability-lxml
"""

import sys
import re
import requests
from bs4 import BeautifulSoup
from readability import Document

# Helper to strip unwanted tags
def clean_soup(soup: BeautifulSoup) -> BeautifulSoup:
    # Remove scripts, styles, noscript
    for tag in soup(['script', 'style', 'noscript', 'iframe', 'form']):
        tag.decompose()
    # Remove elements with ids or classes that contain common ad or nav keywords
    keywords = [
        'ad', 'ads', 'sponsor', 'banner', 'footer', 'header', 'nav', 'sidebar', 'menu',
        'related', 'comments', 'share', 'twitter', 'facebook', 'newsletter', 'subscribe',
        'popup', 'cookie', 'widget', 'social', 'promo'
    ]
    pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.I)
    for tag in soup.find_all(attrs=lambda attr: attr and pattern.search(attr)):
        tag.decompose()
    return soup


def main(url: str):
    # Use a common user‑agent to avoid basic bot blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CleanArticle/1.0; +https://github.com/yourrepo)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)

    # Try readability first
    doc = Document(resp.text)
    title = doc.title()
    summary_html = doc.summary()

    if not summary_html or summary_html.strip() == "":
        # Fallback: strip tags from the raw HTML
        soup = BeautifulSoup(resp.text, 'html.parser')
        summary_html = "".join([p.get_text(separator='\n', strip=True) for p in soup.find_all('p')])
        if not summary_html:
            summary_html = resp.text

    soup = BeautifulSoup(summary_html, 'html.parser')
    clean = clean_soup(soup)

    text = clean.get_text(separator='\n', strip=True)
    if not text:
        # Final fallback: use all text from original page
        text = BeautifulSoup(resp.text, 'html.parser').get_text(separator='\n', strip=True)
    print(f"Title: {title}\n\n{text}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_article.py <url>")
        sys.exit(1)
    main(sys.argv[1])
