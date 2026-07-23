from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse, urlunparse

def extract_links(html: str, url: str) -> set[str]:
    soup = BeautifulSoup(html,"html.parser")
    link_set: set[str] = set()

    for tag in soup.find_all("a"):
        href = tag.get("href")
        if not isinstance(href, str):
            continue
        href = href.strip()
        if not href:
            continue
        link = urljoin(url,href)
        if not link.startswith(("http://", "https://")):
            continue
        clean_url, _ = urldefrag(link)
        clean_url = normalise_url(clean_url)
        link_set.add(clean_url)

    return link_set

def normalise_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    host = parsed.hostname.lower() if parsed.hostname else ""
    path = parsed.path

    if not path:
        path = '/'

    port = parsed.port

    if port is None or (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        netloc = host
    else:
        netloc = f"{host}:{port}"

    normalised_url = urlunparse(
        (
            scheme,
            netloc,
            path,
            parsed.params,
            parsed.query,
            ""
        )
    )

    return normalised_url

def is_same_domain(url:str, base:str):
    parsed = urlparse(url)
    base_parsed = urlparse(base)
    host_name = parsed.hostname
    base_host_name = base_parsed.hostname
    if not host_name:
        return False
    if(host_name == base_host_name):
        return True
    else:
        return False
    

