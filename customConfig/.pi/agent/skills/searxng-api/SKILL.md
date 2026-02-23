---
name: searxng-api
description: Guide for using the SearXNG search API. Use when you need to programmatically query SearXNG instances via HTTP.
user-invocable: true
---

# SearXNG API Skill

This skill provides instructions and examples for consuming the SearXNG search API. It covers both GET and POST usage, supported formats, and parameter details.

## Quick Start

Use cURL to query the local SearXNG instance at `http://192.168.1.6:4000`.

```bash
# GET request returning JSON
curl 'http://192.168.1.6:4000/search?q=searxng&format=json'

# POST request returning CSV
curl -X POST 'http://192.168.1.6:4000/search' -d 'q=searxng&format=csv'

# POST request returning JSON with form data
curl -L -X POST -d 'q=searxng&format=json' 'http://192.168.1.6:4000/'
```

## API Reference

SearXNG supports querying via a simple HTTP API. Two endpoints, `/` and `/search`, are supported for both GET and POST methods. The GET method expects parameters as URL query parameters, while the POST method expects parameters as form data.

If you want to consume the results as JSON, CSV, or RSS, you need to set the `format` parameter accordingly. Supported formats are defined in `settings.yml`, under the `search` section. Requesting an unset format will return a 403 Forbidden error. Be aware that many public instances have these formats disabled.

Endpoints:

`GET /` `GET /search`

`POST /` `POST /search`

## Parameters

`q` required

The search query. This string is passed to external search services. Thus, SearXNG supports syntax of each search service. For example, `site:github.com SearXNG` is a valid query for Google. However, if simply the query above is passed to any search engine which does not filter its results based on this syntax, you might not get the results you wanted.

`categories` optional

Comma separated list, specifies the active search categories

`engines` optional

Comma separated list, specifies the active search engines 

`language`

Code of the language. 

`pageno` default `1`

Search page number.

`time_range` optional

[ `day`, `month`, `year` ]

Time range of search for engines which support it. See if an engine supports time range search in the preferences page of an instance.

`format` optional

[ `json`, `csv`, `rss` ]

Output format of results.

`safesearch`

[ `0`, `1`, `2` ]

Filter search results of engines which support safe search. See if an engine supports safe search in the preferences page of an instance.

### Project Links

* [Source](https://github.com/searxng/searxng/tree/master)
* [Wiki](https://github.com/searxng/searxng/wiki)
* [Public instances](http://localhost:4000)
* [Issue Tracker](https://github.com/searxng/searxng/issues)

## Scrape Article

In addition to querying the search API, you can use the **article‑cleaner** tool to fetch the top result and extract the main article text. Use the `article-cleaner` command after obtaining a URL:

## What it does
This skill downloads a URL, parses the HTML, and outputs a cleaned, plain‑text version of the main article body.

## Usage
```python
# Fetch and clean an article
python clean_article.py "https://example.com/news/awesome-article"
```
The script prints the article title followed by the cleaned text.

## Implementation details
The actual extraction logic lives in `scripts/clean_article.py`. It uses `requests`, `beautifulsoup4`, and `readability-lxml` to:
1. GET the page.
2. Identify the main content block.
3. Remove scripts, styles, iframes, and elements whose class/id contain common ad or navigation keywords.
4. Return a readable text.

## Extending
If you need to handle different output formats (e.g., Markdown, JSON), modify `scripts/clean_article.py` accordingly.
