import requests
from bs4 import BeautifulSoup

# Need to come back to figuring out how to parse whole page.
# Right now just parsing short desc for wiki


def parse_url(url: str) -> str:
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        table = soup.find("div", attrs={"id": "mw-content-text"})
        html_text = table.find(
            "div",
            attrs={"class": "shortdescription nomobile noexcerpt noprint searchaux"},
        )
        return html_text.text
    except:
        return False
