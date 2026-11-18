"""Read the new message from a MIME reply."""
import re
from email.message import Message
from email.header import decode_header
from bs4 import BeautifulSoup


def decode_header_text(value: str) -> str:
    result = []
    for part, charset in decode_header(value or ""):
        if isinstance(part, bytes):
            try:
                part = part.decode(charset or "utf-8", errors="replace")
            except LookupError:
                part = part.decode("utf-8", errors="replace")
        result.append(part)
    return "".join(result)


def message_text(msg: Message) -> str:
    plain, html = [], []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment" or part.get_filename():
            continue
        content_type = part.get_content_type()
        if content_type not in {"text/plain", "text/html"}:
            continue
        payload = part.get_payload(decode=True)
        if not payload:
            continue
        try:
            text = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        except LookupError:
            text = payload.decode("utf-8", errors="replace")
        (plain if content_type == "text/plain" else html).append(text)
    if plain:
        return plain[0]
    if html:
        soup = BeautifulSoup(html[0], "html.parser")
        for tag in soup(["style", "script", "head"]):
            tag.decompose()
        for br in soup.find_all("br"):
            br.replace_with("\n")
        for quote in soup.select("blockquote, div.gmail_quote, div.yahoo_quoted, #divRplyFwdMsg"):
            quote.insert_before("\n> \n")
        return soup.get_text("\n", strip=True)
    return ""


def new_reply_text(body: str) -> str:
    # Only newly written text, never our own CTA/opt-out quoted in the thread.
    if re.search(r"<(?:html|div|p)\b", body or "", re.I):
        body = BeautifulSoup(body, "html.parser").get_text("\n", strip=True)
    result = []
    for line in (body or "").splitlines():
        stripped = line.strip().lstrip("\ufeff")
        if re.match(r"^(?:>|(?:-\s*){3,}$|--\s*$|_{5}|-{3,}\s*(?:Original|Oryginalna)|On .+wrote:|W dniu .+(?:napisał|pisze)|Dnia .+napisał|From:\s|Od:\s)", stripped, re.I):
            break
        result.append(stripped)
    return "\n".join(result).strip()
