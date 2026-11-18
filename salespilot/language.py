from __future__ import annotations

import re

from langdetect import DetectorFactory, LangDetectException, detect


DetectorFactory.seed = 0

SUPPORTED_LANGUAGE_CODES = {"pl", "en", "de", "fr", "es", "it", "nl", "cs", "sk", "uk"}
LANGUAGE_NAMES = {
    "pl": "Polish", "en": "English", "de": "German", "fr": "French", "es": "Spanish",
    "it": "Italian", "nl": "Dutch", "cs": "Czech", "sk": "Slovak", "uk": "Ukrainian",
}
LANGUAGE_ALIASES = {
    "polish": "pl", "polski": "pl", "pl-pl": "pl", "english": "en", "angielski": "en", "en-us": "en", "en-gb": "en",
    "german": "de", "deutsch": "de", "french": "fr", "français": "fr", "spanish": "es", "español": "es",
    "italian": "it", "italiano": "it", "dutch": "nl", "czech": "cs", "slovak": "sk", "ukrainian": "uk",
}


def normalize_language(value: str | None) -> str:
    raw = (value or "").strip().lower().replace("_", "-")
    if not raw:
        return "auto"
    raw = LANGUAGE_ALIASES.get(raw, raw.split("-", 1)[0])
    return raw if raw in SUPPORTED_LANGUAGE_CODES else "auto"


def detect_offer_language(text: str, explicit: str | None = None) -> str:
    normalized = normalize_language(explicit)
    if normalized != "auto":
        return normalized
    sample = re.sub(r"https?://\S+|\S+@\S+|[^\w\sąćęłńóśźżÄÖÜßà-ÿЀ-ӿ]", " ", text or "")
    sample = re.sub(r"\s+", " ", sample).strip()[:12000]
    if len(sample) < 35:
        return "en"
    polish_signals = len(re.findall(r"[ąćęłńóśźż]", sample.lower())) + sum(
        3 for word in ("obowiązki", "wymagania", "oferujemy", "doświadczenie", "stanowisko", "praca") if word in sample.lower()
    )
    if polish_signals >= 4:
        return "pl"
    try:
        code = normalize_language(detect(sample))
        return "en" if code == "auto" else code
    except LangDetectException:
        return "en"


def language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(normalize_language(code), "English")
