"""Coletor inicial para páginas de Relações com Investidores (RI).

Escopo intencionalmente mínimo:
- baixa a página principal de RI;
- identifica links com palavras-chave de proventos/dividendos/JCP;
- baixa o conteúdo textual desses links.
"""

from __future__ import annotations

from datetime import datetime
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

KEYWORDS = [
    "divid",
    "jcp",
    "juros sobre capital",
    "provento",
    "remunera",
    "capital próprio",
    "capital proprio",
]


def _parse_date_from_text(text: str):
    for token in text.split():
        token = token.strip(".,;:()[]{}")
        try:
            return datetime.strptime(token, "%d/%m/%Y").date()
        except ValueError:
            continue
    return None


def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return soup.get_text(" ", strip=True)


def _candidate_links(base_url: str, html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    items = []
    seen = set()

    for anchor in soup.select("a[href]"):
        href = (anchor.get("href") or "").strip()
        text = anchor.get_text(" ", strip=True)
        if not href:
            continue

        probe = f"{text} {href}".lower()
        if not any(keyword in probe for keyword in KEYWORDS):
            continue

        full_url = urljoin(base_url, href)
        if full_url in seen:
            continue

        seen.add(full_url)
        items.append({"url": full_url, "hint_title": text})

    return items


def fetch_ri_documents(ri_url: str, max_documents: int = 10) -> list[dict]:
    client = httpx.Client(timeout=20.0, follow_redirects=True)
    try:
        response = client.get(ri_url)
        response.raise_for_status()
    except httpx.HTTPError:
        return []

    links = _candidate_links(ri_url, response.text)
    documents: list[dict] = []

    for item in links[:max_documents]:
        try:
            doc_response = client.get(item["url"])
            doc_response.raise_for_status()
        except httpx.HTTPError:
            continue

        raw_text = _extract_text(doc_response.text)
        if not raw_text:
            continue

        title = item["hint_title"] or item["url"]
        published_at = _parse_date_from_text(raw_text[:6000])
        documents.append(
            {
                "source_type": "ri",
                "url": item["url"],
                "title": title[:500],
                "published_at": published_at,
                "raw_text": raw_text[:120000],
            }
        )

    client.close()
    return documents
