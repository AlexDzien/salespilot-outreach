import unittest

from salespilot.language import detect_offer_language, language_name


class OfferLanguageTest(unittest.TestCase):
    def test_explicit_locale_is_authoritative(self):
        self.assertEqual(detect_offer_language("Short job title", "de-DE"), "de")

    def test_polish_signals_survive_links_and_contact_removal(self):
        description = (
            "Stanowisko: inżynier oprogramowania. Wymagania obejmują doświadczenie "
            "w integracji usług. https://example.com/jobs jobs@example.com"
        )
        self.assertEqual(detect_offer_language(description), "pl")

    def test_short_text_uses_documented_fallback(self):
        self.assertEqual(language_name(detect_offer_language("API Engineer")), "English")
