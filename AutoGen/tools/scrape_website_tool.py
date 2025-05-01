'''
This code is largely based on CrewAI’s scrape_website_tool and is used to extract content from a website.
https://github.com/crewAIInc/crewAI-tools/tree/main/crewai_tools/tools/scrape_website_tool
'''
import re
from typing import Any, Optional, Type

import requests
from bs4 import BeautifulSoup


class ScrapeWebsiteTool():
    name: str = "Read website content"
    description: str = "A tool that can be used to read a website content."
    cookies: Optional[dict] = None
    headers: Optional[dict] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


    def scrape_website(self, website_url:str) -> str:
        page = requests.get(
            website_url,
            timeout=15,
            headers=self.headers,
            cookies=self.cookies if self.cookies else {},
        )

        page.encoding = page.apparent_encoding
        parsed = BeautifulSoup(page.text, "html.parser")

        text = parsed.get_text(" ")
        text = re.sub("[ \t]+", " ", text)
        text = re.sub("\\s+\n\\s+", "\n", text)
        return text

def scrape_website(website_url:str) -> str:
    ''' A tool that can be used to read a website content.'''
    return ScrapeWebsiteTool().scrape_website(website_url)