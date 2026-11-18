# SalesPilot — research ofert i spersonalizowany outreach

Sales workflow for opportunity research, multilingual drafts, delivery evidence, and a CRM board.

**Zakres publiczny:** Studium przypadku, moduł językowy i testy.

## Problem

SalesPilot łączy wyszukiwanie ofert i firm, przygotowanie spersonalizowanych wiadomości oraz śledzenie odpowiedzi w jednym panelu. Operator widzi, które firmy przeszły research, skąd pochodzi kontakt i dlaczego przygotowano dany szkic.

## Jak działa projekt

1. Przebieg researchu pobiera dane z adapterów API, RSS i publicznych źródeł, normalizuje oferty oraz wykrywa duplikaty.
2. Silnik ustala język i wybiera kontekst firmy oraz odpowiednie projekty z portfolio. Projekt wiadomości można sprawdzić w podglądzie.
3. Kolejka i tryb Dry Run rozdzielają przygotowanie od wysyłki SMTP. Identyfikacja odpowiedzi w IMAP pozwala anulować oczekujący follow-up, a lista wykluczeń zatrzymuje już zakolejkowany kontakt.
4. Kanban, metryki przebiegów i dziennik zdarzeń pomagają powiązać ofertę, wiadomość i wynik rozmowy.

## Technologie

FastAPI, React, TypeScript, SQLAlchemy, Alembic, SQLite, APScheduler, REST/SSE, SMTP/IMAP i opcjonalnie Ollama.

## Co można sprawdzić

`salespilot/language.py` to wydzielony moduł sprawdzania języka używany przy tworzeniu szkiców. **Python 3.10+:** `python -m pip install -r requirements.txt`, następnie `python -m unittest discover -s tests`.
